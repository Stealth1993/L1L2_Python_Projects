import numpy as np
import matplotlib.pyplot as plt

# Parameters
x = np.linspace(-10, 10, 1000)
t = 0  # Time snapshot
m = 1  # Mass
k = 1  # Wave number
omega = np.sqrt(k**2 + m**2)

# Klein-Gordon solution (real part)
phi = np.cos(k * x - omega * t)

# Plot
plt.plot(x, phi)
plt.title('Klein-Gordon Equation: Scalar Field Wave')
plt.xlabel('Position (x)')
plt.ylabel('Field Amplitude (φ)')
plt.grid(True)
plt.show()