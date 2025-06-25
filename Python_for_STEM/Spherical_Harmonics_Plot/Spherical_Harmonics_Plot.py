import numpy as np
import matplotlib.pyplot as plt
from scipy.special import sph_harm

# Param
theta = np.linspace(0, np.pi, 100)
phi = np.linspace(0, 2 * np.pi, 100)
theta, phi = np.meshgrid(theta, phi)
l, m = 2, 1 # Quantum numbers

# Spherical Harmonics
Y = sph_harm(m, l, phi, theta)
Y_real = np.real(Y)

# Convert to Cartesian for plotting
x = np.sin(theta) * np.cos(phi) * Y_real
y = np.sin(theta) * np.sin(phi) * Y_real
z = np.cos(theta) * Y_real

# Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis')
ax.set_title(f'Spherical Harmonic Y_{1}^{m}')
plt.show()