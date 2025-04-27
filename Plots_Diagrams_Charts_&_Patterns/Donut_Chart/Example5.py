import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import matplotlib.cm as cm
import matplotlib.colors as colors
import xlsxwriter # Import xlsxwriter
import os # Import os for removing temporary files

# --- Define the CSV file path ---
csv_file_path = 'Test_Data.csv'

# --- Read Data from CSV ---
try:
    df = pd.read_csv(csv_file_path, index_col='CHANNEL')
except FileNotFoundError:
    print(f"Error: CSV file not found at '{csv_file_path}'.")
    exit()
except Exception as e:
    print(f"An error occurred while reading the CSV file: {e}")
    exit()

print("Original Data Head:")
print(df.head())

# --- Data Cleaning: Ensure percentage columns are numeric ---
print("\nCleaning data: Removing '%' and converting to numbers...")
for col in df.columns:
    df[col] = df[col].astype(str).str.replace('%', '', regex=False)
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(0)

# Re-normalize if values were out of 100 after cleaning
for col in df.columns:
     if pd.api.types.is_numeric_dtype(df[col]):
         if df[col].sum() > 0 and df[col].max() > 1 and abs(df[col].sum() - 100) < 10:
              df[col] = df[col] / 100.0
              print(f"Info: Divided values in column '{col}' by 100 (assuming they were out of 100).")

month_labels = df.columns.tolist()
print("\nData after cleaning:")
print(df.head())
num_months = len(month_labels)

if num_months == 0:
    print("No months found in the data.")
    exit()

# --- Filter out the 'Total' row for charts ---
df_charts = df[df.index.str.lower() != 'total'].copy()

# --- Prepare Explode ---
explode_list = [0] * num_months

# --- Create a custom colormap (Red to Green) ---
cmap = colors.LinearSegmentedColormap.from_list("red_green_cmap", ["red", "green"])

# --- Create Excel Workbook and Worksheet ---
excel_file_path = 'donut_charts_excel_report.xlsx'
workbook = xlsxwriter.Workbook(excel_file_path)
worksheet = workbook.add_worksheet('Donut Charts') # Sheet for charts

# --- Add a sheet for the Data Table ---
worksheet_data = workbook.add_worksheet('Data Table')
# Write the DataFrame to the 'Data Table' sheet
# reset_index() is needed to include the 'CHANNEL' index as a column
worksheet_data.write_row(0, 0, ['CHANNEL'] + month_labels) # Write header row manually to include index name
for row_num, (index, row_data) in enumerate(df.iterrows()):
    worksheet_data.write_string(row_num + 1, 0, index) # Write index (channel name)
    worksheet_data.write_row(row_num + 1, 1, row_data.tolist()) # Write row data


# --- Generate and Insert Donut Charts into Excel ---
print("\nGenerating and inserting donut charts into Excel...")
chart_index = 0
cols_per_row = 3
image_height_excel_rows = 25 # Approximate height of each chart in Excel rows
image_width_excel_cols = 15 # Approximate width of each chart in Excel columns

for channel_name, row in df_charts.iterrows():

    # Create a figure for the current donut chart
    fig, ax = plt.subplots(figsize=(4, 4)) # Adjust figure size for individual chart

    sales_percentage_data = row.tolist()

    if np.nansum(sales_percentage_data) == 0:
         # Handle no data case (optional: maybe write text in Excel cell instead of chart)
         print(f"Info: No sales data for channel '{channel_name}'. Skipping chart.")
         chart_index += 1
         plt.close(fig) # Close the empty figure
         continue

    # --- Dynamic Color Generation ---
    min_sale = min(sales_percentage_data)
    max_sale = max(sales_percentage_data)
    norm = colors.Normalize(vmin=min_sale, vmax=max_sale)
    scalar_mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
    dynamic_colors = [scalar_mappable.to_rgba(sale) for sale in sales_percentage_data]

    # --- Create the pie chart on the axes ---
    wedges, texts, autotexts = ax.pie(sales_percentage_data,
                                      explode=explode_list,
                                      labels=month_labels,
                                      colors=dynamic_colors,
                                      autopct='%1.1f%%',
                                      shadow=True,
                                      startangle=140,
                                      pctdistance=0.85,
                                      wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})

    # --- Adjust Autotext (Percentage Label) Colors ---
    for i, autotext in enumerate(autotexts):
        wedge_color = wedges[i].get_facecolor()
        r, g, b, a = wedge_color
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        if luminance < 0.4:
            autotext.set_color('white')
        else:
            autotext.set_color('black')

    # Draw a white circle at the center
    centre_circle = patches.Circle((0, 0), 0.70, color='white')
    ax.add_patch(centre_circle)

    ax.set_aspect('equal')
    ax.set_title(f'{channel_name}')

    for text in texts:
        text.set_fontsize(7)
    for autotext in autotexts:
         autotext.set_fontsize(7)

    # --- Save the figure to a temporary image file ---
    image_file = f'temp_donut_chart_{channel_name.replace(" ", "_").replace("/", "_")}.png'
    try:
        plt.savefig(image_file, bbox_inches='tight')
        plt.close(fig) # Close the figure after saving

        # --- Insert the image into the Excel worksheet ---
        row_index = chart_index // cols_per_row
        col_index = chart_index % cols_per_row

        # Calculate the cell address for insertion
        insert_row = row_index * image_height_excel_rows # Start row for the group
        insert_col = col_index * image_width_excel_cols # Start column for the group

        worksheet.insert_image(insert_row, insert_col, image_file)

        # --- Delete the temporary image file ---
        os.remove(image_file)

        print(f"Inserted chart for {channel_name} into Excel.")

    except Exception as e:
        print(f"Error saving or inserting chart for {channel_name}: {e}")
        # Ensure figure is closed even if saving/inserting fails
        try:
            plt.close(fig)
        except:
            pass

    chart_index += 1 # Increment chart index

# --- Close the Excel Workbook ---
workbook.close()

print(f"\nExcel report '{excel_file_path}' created successfully with donut charts.")