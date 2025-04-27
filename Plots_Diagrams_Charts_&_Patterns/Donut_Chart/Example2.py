import pandas as pd
import matplotlib.pyplot as plt

csv_file_path = 'Test_Data.csv'
df = pd.read_csv(csv_file_path, index_col='CHANNEL')

print(df.head())

month_labels = df.columns.tolist()
num_months = len(month_labels)

print("Cleaning data: Removing '%' and converting to numbers...")
for col in df.columns: # Iterate through each column (which are your months)
    df[col] = df[col].astype(str)
    df[col] = df[col].str.replace('%', '', regex=False)
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(0)  # Fill NaN values with 0

for col in df.columns: # Iterate through each column (which are your months)
    if pd.api.types.is_numeric_dtype(df[col]):
        if df[col].max() > 0:
            df[col] = df[col] / df[col].max() * 100
        else:
            df[col] = 0

month_labels = df.columns.tolist()
print("Data after cleaning:")
print(df.head())
num_months = len(month_labels)

if num_months == 0:
    print("No months found in the data.")
    exit()

base_colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#FFD700', '#FF69B4', '#8A2BE2', '#7FFF00', '#D2691E', '#FF4500']
colors = base_colors * (num_months // len(base_colors) + 1)  # Repeat colors if needed
explode_list = [0.1] * num_months  # Explode all slices

print("Creating donut chart...")

for channel_name, row in df.iterrows():
    plt.figure(figsize=(8, 8))
    plt.pie(row, explode=explode_list, labels=month_labels, colors=colors[:num_months],
            autopct='%1.1f%%', shadow=True, startangle=140)
    
    # Draw a white circle at the center to make it a donut chart
    centre_circle = plt.Circle((0, 0), 0.70, color='white')
    fig = plt.gcf()
    ax = fig.gca()
    ax.add_artist(centre_circle)
    
    # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.gca().set_aspect('equal')  
    
    # Title with channel name
    plt.title(f'Donut Chart for {channel_name}')
    
    # Save the figure
    plt.savefig(f'donut_chart_{channel_name}.png')
    
    # Show the plot

    plt.savefig(f'donut_chart_{channel_name}.png')
    print(f"Donut chart for {channel_name} saved as donut_chart_{channel_name}.png")
