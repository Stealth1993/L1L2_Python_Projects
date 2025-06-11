import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parameters
M = 1.0  # Mass
r0 = 10.0  # Initial radius
phi_dot0 = 0.1  # Initial angular velocity

# Geodesic equations
def geodesic_equations(y, t):
    r, phi, r_dot, phi_dot = y
    r_ddot = r * phi_dot**2 - M / r**2 + 3 * M * r_dot**2 / r**2
    phi_ddot = -2 * r_dot * phi_dot / r
    return [r_dot, phi_dot, r_ddot, phi_ddot]

# Initial conditions
y0 = [r0, 0.0, 0.0, phi_dot0]  # [r, phi, r_dot, phi_dot]
t = np.linspace(0, 100, 1000)  # Time array

# Solve the geodesic equations
solution = odeint(geodesic_equations, y0, t)
r, phi = solution[:, 0], solution[:, 1]

# Convert polar coordinates to Cartesian for plotting
x = r * np.cos(phi)
y = r * np.sin(phi)

# Plotting the geodesic path
plt.figure(figsize=(8, 8))
plt.plot(x, y)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Geodesic Path')
plt.axis('equal')
plt.grid()
plt.show()

# This code simulates the geodesic path of a particle in a Schwarzschild spacetime, plotting its trajectory in Cartesian coordinates.
# The geodesic equations are derived from the Schwarzschild metric, and the particle's motion is influenced by the gravitational field of a massive body.
# The initial conditions and parameters can be adjusted to explore different geodesic paths.
# The code uses the `odeint` function from `scipy.integrate` to numerically solve the differential equations governing the geodesic motion.
# The resulting plot shows the trajectory of the particle in a two-dimensional plane, illustrating how it moves under the influence of gravity.