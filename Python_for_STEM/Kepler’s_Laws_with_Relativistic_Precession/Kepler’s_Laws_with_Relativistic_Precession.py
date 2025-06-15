import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parameters
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
M = 1.989e30    # Mass of the Sun (kg)
c = 3e8         # Speed of light (m/s)
phi = np.linspace(0, 20 * np.pi, 1000)  # Angle parameter for the orbit

# Relativistic orbit equation
def orbit(y, phi):
    r = y[0]
    v = y[1]
    dr_dphi = v
    dv_dphi = -G * M / r**2 * (1 + 3 * G * M / (c**2 * r))  # Including relativistic correction
    return [dr_dphi, dv_dphi]

# Solve the orbit using odeint
def solve_orbit(initial_conditions, phi):
    return odeint(orbit, initial_conditions, phi)

# Initial conditions: [r0, v0]
initial_conditions = [1.496e11, 29780]  # Initial distance (m) and velocity (m/s)
result = solve_orbit(initial_conditions, phi)
# Extract results
r = result[:, 0]
v = result[:, 1]
# Convert polar coordinates to Cartesian for plotting
x = r * np.cos(phi)
y = r * np.sin(phi)
# Plotting the orbit
plt.figure(figsize=(10, 10))
plt.plot(x, y, label='Relativistic Orbit')

plt.title('Relativistic Precession of Planetary Orbits')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.axis('equal')
plt.grid()
plt.legend()
plt.show()