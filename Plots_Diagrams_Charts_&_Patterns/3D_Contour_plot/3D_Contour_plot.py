import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

def f(x, y):
    return np.sin(np.sqrt(x**2 + y**2))
Z = f(X, Y)
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
contour = ax.contour3D(X, Y, Z, 50, cmap='viridis')

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('3D Contour Plot')
plt.colorbar(contour, ax=ax, shrink=0.5, aspect=10)
plt.show()