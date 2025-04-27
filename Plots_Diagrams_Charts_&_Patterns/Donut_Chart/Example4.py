import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.patches as patches
import matplotlib.cm as cm
import matplotlib.colors as colors

# --- Define the CSV file path ---
csv_file_path = 'Test_Data.csv' # Make sure this matches your filename

# --- Read Data from CSV ---
try:
    df = pd.read_csv(csv_file_path, index_col='CHANNEL')
except FileNotFoundError:
    print(f"Error: CSV file not found at '{csv_file_path}'.")
    exit()
except Exception as e:
    print(f"An error occurred while reading the CSV file: {e}")
    exit()

print(df.head())

# --- Data Cleaning: Ensure percentage columns are numeric ---
print("Cleaning data: Removing '%' and converting to numbers...")
for col in df.columns:
    df[col] = df[col].astype(str).str.replace('%', '', regex=False)
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(0) # Fill NaN values with 0

# Re-normalize if values were out of 100 after cleaning (assuming original data sum to 100%)
for col in df.columns:
     if pd.api.types.is_numeric_dtype(df[col]):
         if df[col].sum() > 0 and df[col].max() > 1 and abs(df[col].sum() - 100) < 10: # Simple heuristic
              df[col] = df[col] / 100.0
              print(f"Info: Divided values in column '{col}' by 100 (assuming they were out of 100).")


month_labels = df.columns.tolist() # Get column headers after cleaning
print("Data after cleaning:")
print(df.head())
num_months = len(month_labels)

if num_months == 0:
    print("No months found in the data.")
    exit()

# --- Prepare Explode (based on the number of months) ---
explode_list = [0] * num_months # No explosion by default

# --- Create a custom colormap (Red to Green) ---
cmap = colors.LinearSegmentedColormap.from_list("red_green_cmap", ["red", "green"])

# --- Create PDF file ---
pdf_file_path = 'Sales_charts_report.pdf'
with PdfPages(pdf_file_path) as pdf:

    # --- Page 1: Data Table ---
    fig_table, ax_table = plt.subplots(figsize=(12, len(df) * 0.3 + 2)) # Adjust figure size
    ax_table.axis('off') # Hide axes for the table

    table = ax_table.table(cellText=df.values,
                           rowLabels=df.index,
                           colLabels=df.columns,
                           loc='center',
                           cellLoc='center',
                           rowLoc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(8) # Set font size for table cells
    table.scale(1, 1.5) # Adjust cell height

    ax_table.set_title('Original Data Table', fontsize=14, pad=20)

    pdf.savefig(fig_table, bbox_inches='tight')
    plt.close(fig_table)

    # --- Page 2: Donut Charts Grid with Dynamic Colors ---
    df_charts = df[df.index.str.lower() != 'total'].copy()

    num_channels = len(df_charts)
    cols = 3
    rows = (num_channels + cols - 1) // cols if num_channels > 0 else 1

    fig_charts, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))

    if rows * cols > 1:
        axes = axes.flatten()
    else:
        axes = [axes]

    chart_index = 0
    for channel_name, row in df_charts.iterrows():
        ax = axes[chart_index]
        sales_percentage_data = row.tolist()

        if np.nansum(sales_percentage_data) == 0:
             ax.text(0.5, 0.5, "No Sales Data", horizontalalignment='center', verticalalignment='center', fontsize=12)
             ax.set_title(f'{channel_name}')
             ax.axis('off')
             chart_index += 1
             continue

        # --- Dynamic Color Generation based on Sales Percentage for THIS CHANNEL ---
        min_sale = min(sales_percentage_data)
        max_sale = max(sales_percentage_data)

        norm = colors.Normalize(vmin=min_sale, vmax=max_sale)
        scalar_mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
        dynamic_colors = [scalar_mappable.to_rgba(sale) for sale in sales_percentage_data]

        # --- Create the pie chart on the current axes (subplot) ---
        wedges, texts, autotexts = ax.pie(sales_percentage_data,
                                          explode=explode_list,
                                          labels=month_labels,
                                          colors=dynamic_colors, # Use the dynamically generated colors
                                          autopct='%1.1f%%',
                                          shadow=True,
                                          startangle=140,
                                          pctdistance=0.85)

        # --- Adjust Autotext (Percentage Label) Colors for Readability ---
        for i, autotext in enumerate(autotexts):
            # Get the color of the wedge (slice) corresponding to this autotext
            wedge_color = wedges[i].get_facecolor()

            # Calculate luminance (perceived brightness) of the color
            # Using a common formula for sRGB colors
            r, g, b, a = wedge_color
            luminance = 0.299 * r + 0.587 * g + 0.114 * b

            # Set text color based on luminance threshold
            # Adjust the threshold (e.g., 0.4) based on what looks best
            if luminance < 0.4:
                autotext.set_color('white')
            else:
                autotext.set_color('black') # You could use '#333333' for dark gray

        # Draw a white circle at the center to make it a donut chart on the axes
        centre_circle = patches.Circle((0, 0), 0.70, color='white')
        ax.add_patch(centre_circle)

        ax.set_aspect('equal')
        ax.set_title(f'{channel_name}')

        # Adjust label sizes for clarity in subplots
        for text in texts:
            text.set_fontsize(7)
        for autotext in autotexts:
             autotext.set_fontsize(7)


        chart_index += 1

    for i in range(chart_index, len(axes)):
        fig_charts.delaxes(axes[i])

    fig_charts.suptitle('Monthly Sales Percentage Distribution by Channel', fontsize=16, y=1.02)
    fig_charts.tight_layout(rect=[0, 0.03, 1, 0.95])

    pdf.savefig(fig_charts, bbox_inches='tight')
    plt.close(fig_charts)

print(f"PDF report '{pdf_file_path}' created successfully.")