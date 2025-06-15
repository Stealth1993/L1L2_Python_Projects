import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Description: This program solves null geodesic equations in Kerr spacetime, incorporating
# the Carter constant for a more accurate trajectory.

# Parameters
M, a = 1.0, 0.9  # Mass, Spin parameter
phi = np.linspace(0, 4 * np.pi, 1000)

# Kerr metric functions
def delta(r):
    return r**2 - 2 * M * r + a**2

# Geodesic ODE with Carter constant (simplified)
def geodesic(y, phi, L, Q):
    r, dr = y
    V_eff = (L**2 + Q - (2 * M * r * L**2) / delta(r)) / r**2
    d2r = -M / delta(r) + V_eff
    return [dr, d2r]

# Solve for a null geodesic
L, Q = 3.0, 10.0  # Angular momentum, Carter constant
sol = odeint(geodesic, [5.0, 0], phi, args=(L, Q))
r = sol[:, 0]
x, y = r * np.cos(phi), r * np.sin(phi)

# Ergosphere
r_ergo = M + np.sqrt(M**2 - a**2 * np.cos(phi)**2)

# Plot
plt.figure(figsize=(8, 8))
plt.plot(r_ergo * np.cos(phi), r_ergo * np.sin(phi), 'r--', label='Ergosphere')
plt.plot(x, y, 'b-', label='Null Geodesic')
plt.title('Kerr Black Hole Geodesics with Carter Constant')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()