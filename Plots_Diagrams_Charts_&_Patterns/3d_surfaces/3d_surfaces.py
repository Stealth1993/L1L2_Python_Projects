import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create meshgrid
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)

# Create figure with subplots
fig = plt.figure(figsize=(15, 12))

# Surface 1: Paraboloid
ax1 = fig.add_subplot(221, projection='3d')
Z1 = X**2 + Y**2
surf1 = ax1.plot_surface(X, Y, Z1, cmap='viridis')
fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=5)
ax1.set_title('Surface 1: Paraboloid')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')

# Surface 2: Saddle Surface
ax2 = fig.add_subplot(222, projection='3d')
Z2 = X**2 - Y**2
surf2 = ax2.plot_surface(X, Y, Z2, cmap='plasma')
fig.colorbar(surf2, ax=ax2, shrink=0.5, aspect=5)
ax2.set_title('Surface 2: Saddle Surface')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')

# Surface 3: Ripple
ax3 = fig.add_subplot(223, projection='3d')
Z3 = np.sin(np.sqrt(X**2 + Y**2))
surf3 = ax3.plot_surface(X, Y, Z3, cmap='coolwarm', alpha=0.8)
ax3.set_title('Ripple: z = sin(√(x² + y²))')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')

# Surface 4: Mexican Hat
ax4 = fig.add_subplot(224, projection='3d')
R = np.sqrt(X**2 + Y**2)
Z4 = np.exp(-R**2/4) * np.cos(2*R)
surf4 = ax4.plot_surface(X, Y, Z4, cmap='hot', alpha=0.8)
ax4.set_title('Mexican Hat: z = e^(-r²/4)cos(2r)')
ax4.set_xlabel('X')
ax4.set_ylabel('Y')
ax4.set_zlabel('Z')

plt.tight_layout()
plt.show()