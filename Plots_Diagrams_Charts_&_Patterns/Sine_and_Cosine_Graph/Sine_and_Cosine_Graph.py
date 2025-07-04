import numpy as np
import matplotlib.pyplot as plt

# Generate x values from 0 to 2π
x = np.linspace(0, 2 * np.pi, 100)

# Calculate sine and cosine values
y1 = np.sin(x)
y2 = np.cos(x)

# Create the plot
plt.figure(figsize=(10, 5))
plt.plot(x, y1, label='Sine', color='blue')
plt.plot(x, y2, label='Cosine', color='red')
plt.title('Sine and Cosine Functions')
plt.xlabel('x (radians)')
plt.ylabel('y')
plt.axhline(0, color='black', lw=0.5, ls='--')
plt.axvline(0, color='black', lw=0.5, ls='--')
plt.grid()
plt.legend()
plt.xlim(0, 2 * np.pi)
plt.ylim(-1.5, 1.5)
plt.xticks(np.arange(0, 2 * np.pi + 0.1, np.pi / 2), 
           ['0', 'π/2', 'π', '3π/2', '2π'])
plt.yticks(np.arange(-1, 2, 0.5))
plt.gca().set_aspect('equal', adjustable='box')
plt.tight_layout()
plt.show()