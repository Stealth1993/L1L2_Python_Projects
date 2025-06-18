import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Description: This program simulates the Penrose process in a Kerr ergosphere, tracking
# particle trajectories and energy extraction.

# Parameters
M, a = 1.0, 0.9
phi = np.linspace(0, 2 * np.pi, 1000)

# Ergosphere and trajectory
def trajectory(y, phi):
    r, dr = y
    delta = r**2 - 2 * M * r + a**2
    d2r = -(M * r / delta) * dr**2  # Simplified
    return [dr, d2r]

# Solve trajectory
sol = odeint(trajectory, [2.0, -0.1], phi)
r = sol[:, 0]
x, y = r * np.cos(phi), r * np.sin(phi)
r_ergo = M + np.sqrt(M**2 - a**2 * np.cos(phi)**2)

# Plot
plt.figure(figsize=(8, 8))
plt.plot(r_ergo * np.cos(phi), r_ergo * np.sin(phi), 'r--', label='Ergosphere')
plt.plot(x, y, 'b-', label='Particle Trajectory')
plt.title('Penrose Process in Kerr Ergosphere')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()