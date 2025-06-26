import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters
T, L = 1.0, 1.0 # Tension, Length scale
t = np.linspace(0, 2 * np.pi, 100)
x0, x1 = np.meshgrid(t, t)

# Simplified brane embedding (oscillating in extra dimensions)
X0 = x0 # Time-lile coordinate
X1 = x1 # Spatial coordinate
X2 = np.sin(x0) * np.cos(x1) # Oscillation in 3rd dimension
X3 = np.cos(x0) * np.sin(x1) # 4th dimension (projected)

# Plot 3d projection
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X1, X2, X3, cmap='viridis')
ax.set_title('D3-Brane Dynamics in 10D (3D Projection)')
ax.set_xlabel('X1')
ax.set_ylabel('X2')
ax.set_zlabel('X3')
plt.show()