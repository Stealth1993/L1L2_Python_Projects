import numpy as np
import matplotlib.pyplot as plt

# Sample data (distance in Mpc, velocity in km/s)
distances = np.linspace(1, 100, 50)
H0 = 70  # Hubble constant (km/s/Mpc)
velocities = H0 * distances + np.random.normal(0, 50, distances.size)

# Plot
plt.scatter(distances, velocities, c='blue', label='Galaxies')
plt.plot(distances, H0 * distances, 'r-', label=f'H₀ = {H0} km/s/Mpc')
plt.title('Hubble Diagram: Galaxy Recession')
plt.xlabel('Distance (Mpc)')
plt.ylabel('Velocity (km/s)')
plt.legend()
plt.grid(True)
plt.show()

# This code generates a Hubble diagram showing the relationship between the distance of galaxies and their recession velocity.
# The plot includes a line representing the Hubble constant, illustrating the linear relationship expected in an expanding universe.
# The data is simulated, with some random noise added to the velocities to mimic real observational data.
# The plot is displayed using matplotlib, with labeled axes and a legend for clarity.
# The code is designed to be run in a Python environment with the necessary libraries installed.
# The code is a simple implementation of a Hubble diagram plot using matplotlib.

# Application: Hubble_Diagram_Plot