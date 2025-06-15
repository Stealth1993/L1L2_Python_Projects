import numpy as np
import matplotlib.pyplot as plt

# Parameters
x = np.linspace(-10, 10, 1000)
t = 0
m = 1.0  # Mass parameter
k = 1.0  # Wave number
omega = np.sqrt(k**2 + m**2)  # Frequency

# Klein-Gordon solution (real part)
def phi(x, t):
    return np.sin(k * x - omega * t)

# Calculate the wave function
wave_function = phi(x, t)

# Plotting the wave function
plt.figure(figsize=(10, 6))
plt.plot(x, wave_function, label='t=0s')
plt.xlabel('Position (x)')
plt.ylabel('Wave Function (φ)')
plt.title('Klein-Gordon Wave Function at t=0s')
plt.xlim(-10, 10)
plt.ylim(-1.5, 1.5)
plt.grid(True)
plt.legend()
plt.show()