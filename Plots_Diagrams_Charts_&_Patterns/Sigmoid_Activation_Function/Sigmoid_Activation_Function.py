import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    """Compute the sigmoid activation function."""
    return 1 / (1 + np.exp(-x))

x = np.linspace(-10, 10, 100)
y = sigmoid(x)

plt.plot(x, y, label='Sigmoid Function')
plt.title('Sigmoid Activation Function')   
plt.xlabel('Input')
plt.ylabel('Output')
plt.axhline(0, color='black', lw=0.5, ls='--')
plt.axvline(0, color='black', lw=0.5, ls='--')
plt.grid(alpha=0.3)
plt.legend()
plt.show()