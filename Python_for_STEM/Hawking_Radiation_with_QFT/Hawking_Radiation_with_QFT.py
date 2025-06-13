import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.constants import k as k_B

# Paramaters for the black hole
M0 = 1e15  # Initial mass of the black hole in kg
G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
c = 299792458  # Speed of light in m/s
hbar = 1.0545718e-34  # Reduced Planck's constant in J s
t = np.linspace(0, 1e7, 1000)  # Time array in seconds

# Hawking temperature with QFT corrections
def hawking_temperature(M):
    """Calculate the Hawking temperature with QFT corrections."""
    return (hbar * c**3) / (8 * np.pi * G * M * k_B)

# Hawking radiation rate with QFT corrections
def hawking_radiation_rate(M):
    """Calculate the Hawking radiation rate with QFT corrections."""
    return (hbar**2 * c**4) / (15360 * np.pi * G**2 * M**2)

# Differential equation for the mass loss due to Hawking radiation
def mass_loss(M, t):
    """Differential equation for the mass loss due to Hawking radiation."""
    return -hawking_radiation_rate(M)

# Solve the differential equation
def solve_mass_loss(M0, t):
    """Solve the differential equation for mass loss."""
    M = odeint(mass_loss, M0, t)
    return M.flatten()

# Calculate the mass loss over time
M = solve_mass_loss(M0, t)

# Calculate the Hawking temperature over time
T = hawking_temperature(M)

# Plot the results
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, M, label='Mass (kg)')
plt.xlabel('Time (s)')
plt.ylabel('Mass (kg)')
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(t, T, label='Temperature (K)', color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (K)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()