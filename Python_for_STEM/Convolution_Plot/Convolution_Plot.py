import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve

# Parameters

n = np.arange(0, 10, 0.1)

# Define the two signals
x1 = np.sin(n)  # First signal: sine wave
x2 = np.exp(-n)  # Second signal: exponential decay

# Perform convolution
y = convolve(x1, x2, mode='full')

# Create a new time vector for the convolution result
n_y = np.arange(0, len(y) * 0.1, 0.1)

# Plot the original signals and the convolution result
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(n, x1, label='Sine Wave', color='blue')
plt.title('Original Signals')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(n, x2, label='Exponential Decay', color='orange')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(n_y, y, label='Convolution Result', color='green')
plt.legend()

plt.tight_layout()
plt.show()
# This code generates a plot showing the convolution of a sine wave and an exponential decay function.
# The first two subplots display the original signals, while the third subplot shows the result of their convolution.