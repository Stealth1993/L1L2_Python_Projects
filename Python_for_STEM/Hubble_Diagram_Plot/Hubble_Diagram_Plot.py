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