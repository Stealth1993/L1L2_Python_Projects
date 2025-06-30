import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Matrix

# Description: This program visualizes a traversable wormhole using the Morris-Thorne metric,
# computing the embedding diagram and curvature.

# Parameters
l, phi = np.linspace(-5, 5, 100), np.linspace(0, 2 * np.pi, 100)
L, PHI = np.meshgrid(l, phi)
b0 = 1.0  # Throat radius

# Embedding function
z = np.sqrt(L**2 + b0**2)

# Metric tensor (simplified)
l_sym = symbols('l')
g_tt = -1
g_ll = 1
g_phiphi = b0**2 + l_sym**2
metric = Matrix([[g_tt, 0, 0], [0, g_ll, 0], [0, 0, g_phiphi]])

# Plot embedding
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(L * np.cos(PHI), L * np.sin(PHI), z, cmap='viridis')
ax.set_title('Wormhole Embedding Diagram')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()