import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters for the spheres
r1, r2, r3, r4 = 1, 2, 3, 4
theta = np.linspace(0, 2 * np.pi, 100)
phi = np.linspace(0, np.pi, 100)
THETA, PHI = np.meshgrid(theta, phi)

# Sphere coordinates
x1 = r1 * np.outer(np.cos(THETA), np.sin(PHI))
y1 = r1 * np.outer(np.sin(THETA), np.sin(PHI))
z1 = r1 * np.outer(np.ones(np.size(THETA)), np.cos(PHI))

x2 = r2 * np.outer(np.cos(THETA), np.sin(PHI))
y2 = r2 * np.outer(np.sin(THETA), np.sin(PHI))
z2 = r2 * np.outer(np.ones(np.size(THETA)), np.cos(PHI))

x3 = r3 * np.outer(np.cos(THETA), np.sin(PHI))
y3 = r3 * np.outer(np.sin(THETA), np.sin(PHI))
z3 = r3 * np.outer(np.ones(np.size(THETA)), np.cos(PHI))

x4 = r4 * np.outer(np.cos(THETA), np.sin(PHI))
y4 = r4 * np.outer(np.sin(THETA), np.sin(PHI))
z4 = r4 * np.outer(np.ones(np.size(THETA)), np.cos(PHI))

# Curvatures
k1 = 1 / r1
k2 = 1 / r2
k3 = 1 / r3
k4 = 1 / r4

# Descartes' Theorem
k_total = k1 + k2 + k3 + k4

# Plotting the spheres
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x1, y1, z1, color='r', alpha=0.5, rstride=5, cstride=5)
ax.plot_surface(x2, y2, z2, color='g', alpha=0.5, rstride=5, cstride=5)
ax.plot_surface(x3, y3, z3, color='b', alpha=0.5, rstride=5, cstride=5)
ax.plot_surface(x4, y4, z4, color='y', alpha=0.5, rstride=5, cstride=5)
ax.set_title("Descartes' Theorem with Differential Geometry")
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.text2D(0.05, 0.95, f"Total Curvature: {k_total:.2f}", transform=ax.transAxes, fontsize=14)
plt.show()