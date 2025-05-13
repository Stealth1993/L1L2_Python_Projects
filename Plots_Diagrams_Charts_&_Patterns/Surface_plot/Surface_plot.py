import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a grid of points
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# Create a 3D surface plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

# Generate a random seed and print it
np.random.seed(0)
print("Random seed:", np.random.get_state()[1])
# Add a footer to the plot
#plt.figtext(0.5, 0.01, "Random seed: {}".format(np.random.get_state()[1]), ha="center")
plt.title("3D Surface Plot")
plt.show()