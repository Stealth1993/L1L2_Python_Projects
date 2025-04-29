import matplotlib.pyplot as plt
import numpy as np

x = np.random.rand(1000)
y = np.random.rand(1000)

plt.hexbin(x, y, gridsize=50, cmap='magma')
plt.colorbar(label='Counts in bin')
plt.xlabel('X-axis label')
plt.ylabel('Y-axis label')  

plt.title('Hexabin Plot Example')
plt.show()