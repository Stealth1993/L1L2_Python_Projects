import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2 * np.pi, 360)
x = np.sin(t) * (np.exp(np.cos(t)) - 2 * np.cos(4 * t))
y = np.cos(t) * (np.exp(np.cos(t)) - 2 * np.cos(4 * t))

plt.figure(figsize=(8, 8))

plt.plot(x, y, color='purple', linewidth=2)
plt.plot(-x, y, color='purple', linewidth=2, alpha=0.5)  # Mirror image for the other side
plt.fill(x, y, color='blue', alpha=0.3)  # Fill the butterfly shape

plt.title('Butterfly Pattern', fontsize=20, fontweight='bold')
plt.axis('equal')
plt.axis('off')
plt.show()
