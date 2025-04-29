import matplotlib.pyplot as plt
import numpy as np

x = np.random.rand(1000)
y = np.random.rand(1000)

plt.hexbin(x, y, gridsize=50, cmap='Blues', edgecolors='black')
plt.colorbar(label='Count in bin')

plt.title('Honeycomb Pattern Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

plt.grid(False)  # Disable the grid for a cleaner look
plt.show()