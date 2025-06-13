import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.constants import k as k_B

# Physical constants
G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
c = 299792458    # Speed of light in m/s
hbar = 1.0545718e-34  # Reduced Planck's constant in J s
k_B = 1.380649e-23    # Boltzmann constant in J/K

# Simulation parameters
M0 = 1e7  # Initial black hole mass in kg (chosen for a lifetime of ~10^5 seconds)
t = np.linspace(0, 1e5, 10000)  # Time array from 0 to 100,000 seconds with 10,000 points

# Hawking temperature function
def hawking_temperature(M):
    """Calculate the Hawking temperature of the black hole in Kelvin."""
    return (hbar * c**3) / (8 * np.pi * G * M * k_B)

# Mass loss rate due to Hawking radiation
def hawking_radiation_rate(M):
    """Calculate the mass loss rate in kg/s due to Hawking radiation."""
    return hbar * c**4 / (15360 * np.pi * G**2 * M**2)

# Differential equation for mass loss
def mass_loss(M, t):
    """Define the differential equation dM/dt for mass loss."""
    return -hawking_radiation_rate(M)

# Solve the mass loss differential equation
def solve_mass_loss(M0, t):
    """Solve the mass loss ODE using scipy's odeint."""
    M = odeint(mass_loss, M0, t)
    return M.flatten()

# Compute mass and temperature over time
M = solve_mass_loss(M0, t)
T = hawking_temperature(M)

# Plotting the results
plt.figure(figsize=(12, 6))

# Mass plot
plt.subplot(2, 1, 1)
plt.plot(t, M, label='Mass (kg)')
plt.xlabel('Time (s)')
plt.ylabel('Mass (kg)')
plt.legend()
plt.grid()

# Temperature plot
plt.subplot(2, 1, 2)
plt.plot(t, T, label='Temperature (K)', color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (K)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()