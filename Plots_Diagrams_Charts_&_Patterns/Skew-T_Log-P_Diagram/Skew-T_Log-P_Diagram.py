import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import FuncFormatter
from metpy.plots import SkewT

# Sample data for demonstration
pressure_levels = np.array([1000, 925, 850, 700, 500, 300, 200])  # hPa
temperature = np.array([15, 10, 5, -5, -20, -30, -40])  # Celsius
dew_point = np.array([10, 5, 0, -10, -25, -35, -45])  # Celsius
wind_speed = np.array([5, 10, 15, 20, 25, 30, 35])  # m/s
wind_direction = np.array([0, 45, 90, 135, 180, 225, 270])  # degrees

# Create a Skew-T Log-P plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1, projection='skewx')
skewt = SkewT(ax, rotation=45)
skewt.plot(pressure_levels, temperature, 'r', label='Temperature (°C)')
skewt.plot(pressure_levels, dew_point, 'g', label='Dew Point (°C)')
skewt.plot_barbs(pressure_levels, temperature, wind_speed, wind_direction, color='blue', label='Wind Barbs')
skewt.ax.set_title('Skew-T Log-P Diagram', fontsize=16)
skewt.ax.set_xlabel('Temperature (°C)', fontsize=12)
skewt.ax.set_ylabel('Pressure (hPa)', fontsize=12)
skewt.ax.set_ylim(1000, 100)

# Customize the grid
skewt.ax.xaxis.set_major_locator(MultipleLocator(10))
skewt.ax.xaxis.set_minor_locator(AutoMinorLocator(5))
skewt.ax.yaxis.set_major_locator(MultipleLocator(50))
skewt.ax.yaxis.set_minor_locator(AutoMinorLocator(5))
skewt.ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
skewt.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)} hPa'))
skewt.ax.grid(which='both', linestyle='--', linewidth=0.5)
skewt.ax.legend(loc='upper right', fontsize=10)
skewt.ax.set_xlim(-40, 40)
skewt.ax.set_ylim(1000, 100)

# Show the plot
plt.tight_layout()
plt.show()

