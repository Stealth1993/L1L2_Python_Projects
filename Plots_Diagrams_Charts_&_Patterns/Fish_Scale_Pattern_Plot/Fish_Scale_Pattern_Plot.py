import numpy as np
import matplotlib.pyplot as plt

rows, cols = 10, 10

# Create a grid of points
x = np.linspace(0, 1, cols)
y = np.linspace(0, 1, rows)
X, Y = np.meshgrid(x, y)

# Define the fish scale pattern function
def fish_scale_pattern(x, y):
    return np.sin(3 * np.pi * x) * np.cos(3 * np.pi * y)

Z = fish_scale_pattern(X, Y)

# Plotting the fish scale pattern
plt.figure(figsize=(8, 8))
plt.contourf(X, Y, Z, levels=20, cmap='viridis')
plt.colorbar()
plt.title('Fish Scale Pattern')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()