import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.patches as patches
import matplotlib.ticker as mticker


csv_file_path = 'Test_Data.csv'

try:
    df = pd.read_csv(csv_file_path, index_col='CHANNEL')
except FileNotFoundError:
    print(f"Error: The file {csv_file_path} was not found.")
    exit()
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    exit()

print(df.head())

#Cleaning data: Removing '%' and converting to numbers
# Iterate through each column (which are your months)
print("Cleaning data: Removing '%' and converting to numbers...")
for col in df.columns:
    df[col] = df[col].astype(str).str.replace('%', '', regex=False)
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(0)

# Re-normalize if values were out of 100 after cleaning (optional, but good practice if original data sum to 100%)
for col in df.columns:
     if pd.api.types.is_numeric_dtype(df[col]):
         # Check if column sum is close to 100 and max is > 1 (heuristic for data out of 100)
         if df[col].sum() > 0 and df[col].max() > 1 and abs(df[col].sum() - 100) < 10: # Simple heuristic
             df[col] = df[col] / 100.0
             print(f"Info: Divided values in column '{col}' by 100 (assuming they were out of 100).")

month_labels = df.columns.tolist()
print("Data after cleaning:")
print(df.head())
num_months = len(month_labels)

if num_months == 0:
    print("No months found in the data.")
    exit()

base_colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#FFD700', '#FF69B4', '#8A2BE2', '#7FFF00', '#D2691E', '#FF4500']
colors_list = (base_colors * (num_months // len(base_colors) + 1))[:num_months]  


# --- Create PDF file ---
pdf_file_path = 'Sales_charts_report.pdf'
with PdfPages(pdf_file_path) as pdf:

    # --- Page 1: Data Table ---
    fig_table, ax_table = plt.subplots(figsize=(12, len(df) * 0.3 + 2)) # Adjust figure size
    ax_table.axis('off') # Hide axes for the table

    # Create the table from the DataFrame
    table = ax_table.table(cellText=df.values,
                           rowLabels=df.index,
                           colLabels=df.columns,
                           loc='center',
                           cellLoc='center',
                           rowLoc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(8) # Set font size for table cells
    table.scale(1, 1.5) # Adjust cell height

    ax_table.set_title('Original Data Table', fontsize=14, pad=20) # Title for the table page

    # Save the table figure to the PDF
    pdf.savefig(fig_table, bbox_inches='tight')
    #plt.close(fig_table) # Close the figure to free memory

    # --- Page 2: Donut Charts Grid ---
    # Filter out the 'Total' row for chart creation
    df_charts = df[df.index.str.lower() != 'total'].copy()

    num_channels = len(df_charts)
    cols = 3
    rows = (num_channels + cols - 1) // cols # Calculate number of rows needed

    # Create a large figure to hold all the donut charts as subplots
    fig_charts, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 5)) # Adjust figure size for charts

    # Flatten the axes array if it's 2D to make it easier to iterate
    if rows > 1 or cols > 1:
        axes = axes.flatten()
    elif rows == 1 and cols == 1:
        axes = [axes] # Ensure axes is always an iterable list

    chart_index = 0
    # Iterate through each channel (excluding 'Total') to create its chart on a subplot
    for channel_name, row in df_charts.iterrows():

        # Get the current subplot axes for this chart
        ax = axes[chart_index]

        # row contains numeric sales percentage data for this channel
        sales_percentage_data = row.tolist()

        # Create explode list for this specific chart (e.g., explode based on max value)
        # explode_this_chart = [0] * num_months
        # if sales_percentage_data:
        #    max_value_index = sales_percentage_data.index(max(sales_percentage_data))
        #    explode_this_chart[max_value_index] = 0.1 # Explode the largest slice

        # Use a simple non-exploding list or the exploding list from before
        explode_this_chart = [0] * num_months # No explosion for subplots by default

        # Check if the sum is zero or has invalid data before plotting
        # Use np.nansum to handle potential NaNs if not filled with 0 earlier
        if np.nansum(sales_percentage_data) == 0:
             ax.text(0.5, 0.5, "No Sales Data", horizontalalignment='center', verticalalignment='center', fontsize=12)
             ax.set_title(f'{channel_name}')
             ax.axis('off') # Hide axes for empty chart subplot
             chart_index += 1
             continue # Skip plotting for this channel

        # --- Create the pie chart on the current axes (subplot) ---
        # Pass the cleaned, numerical percentage data.
        wedges, texts, autotexts = ax.pie(sales_percentage_data,
                                          explode=explode_this_chart,
                                          labels=month_labels,
                                          colors=colors_list, # Use colors list for number of months
                                          autopct='%1.1f%%', # Show percentage with one decimal place
                                          shadow=True,
                                          startangle=140,
                                          pctdistance=0.85) # Position percentage labels

        # Draw a white circle at the center to make it a donut chart on the axes
        centre_circle = patches.Circle((0, 0), 0.70, color='white')
        ax.add_patch(centre_circle)

        # Equal aspect ratio ensures the pie is drawn as a circle.
        ax.set_aspect('equal')

        # Title with channel name for the subplot
        ax.set_title(f'{channel_name}') # Title for the individual subplot

        # Adjust label sizes for clarity in subplots
        for text in texts:
            text.set_fontsize(7)
        for autotext in autotexts:
             autotext.set_fontsize(7)

        chart_index += 1 # Increment index for the next subplot

    # Hide any unused subplots if the number of charts is not a perfect multiple of 3
    for i in range(chart_index, len(axes)):
        fig_charts.delaxes(axes[i])

    # Add a main title for the charts page
    fig_charts.suptitle('Monthly Sales Percentage Distribution by Channel', fontsize=16, y=1.02)
    # Adjust layout to prevent overlap and make space for the main title
    fig_charts.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Save the charts grid figure to the PDF
    pdf.savefig(fig_charts, bbox_inches='tight')
    plt.close(fig_charts) # Close the figure

print(f"PDF report '{pdf_file_path}' created successfully.")

# The 'with PdfPages(...)' block automatically closes the PDF file when exiting the block.