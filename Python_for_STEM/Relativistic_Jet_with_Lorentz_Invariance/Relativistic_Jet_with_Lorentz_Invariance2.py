import numpy as np
import matplotlib.pyplot as plt

# Description: This program simulates a relativistic jet with Lorentz-invariant beaming,
# incorporating relativistic Doppler effects.

# Parameters
v = 0.99 * 3e8  # Jet velocity (m/s)
c = 3e8
theta = np.linspace(0, np.pi, 100)
gamma = 1 / np.sqrt(1 - (v / c)**2)

# Beaming factor
beta = v / c
I = 1 / (gamma**2 * (1 - beta * np.cos(theta))**2)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(theta, I, 'b-')
plt.title('Relativistic Jet with Lorentz-Invariant Beaming')
plt.xlabel('Angle (rad)')
plt.ylabel('Intensity (arbitrary units)')
plt.grid(True)
plt.show()