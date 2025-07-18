import tkinter as tk
from tkinter import ttk

def create_gauge_chart():
    # Define the gauge chart configuration
    gauge_config = {
        "type": "doughnut",
        "data": {
            "datasets": [{
                "data": [75, 25],  # Value (75%) and remaining (25%)
                "backgroundColor": ["#36A2EB", "#E0E0E0"],  # Blue for filled, gray for empty
                "borderWidth": 0,
                "circumference": 180,  # Semi-circle for gauge effect
                "rotation": -90  # Start from the bottom
            }],
            "labels": ["Used", "Remaining"]
        },
        "options": {
            "cutout": "80%",  # Makes it look like a gauge
            "rotation": -90,
            "circumference": 180,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "Gauge Chart (75%)",
                    "font": {"size": 18}
                },
                "legend": {
                    "display": False
                }
            },
            "maintainAspectRatio": False
        }
    }

    # Create a new window for the chart
    chart_window = tk.Toplevel(root)
    chart_window.title("Gauge Chart")
    chart_window.geometry("400x300")

    # Placeholder for chart (simulated as a label for now, actual rendering would be via a web view)
    chart_label = tk.Label(chart_window, text="Gauge Chart would be displayed here (75%)\n(Use a browser with Chart.js for full interactivity)")
    chart_label.pack(expand=True)

    # For actual implementation, this JSON would be used in a Chart.js environment
    print("Gauge Chart Config:", gauge_config)

# GUI Setup
root = tk.Tk()
root.title("Gauge Chart Generator")
root.geometry("300x200")

# Button to create gauge chart
btn_create_chart = ttk.Button(root, text="Create Gauge Chart", command=create_gauge_chart)
btn_create_chart.pack(pady=20)

# Start the GUI loop
root.mainloop()