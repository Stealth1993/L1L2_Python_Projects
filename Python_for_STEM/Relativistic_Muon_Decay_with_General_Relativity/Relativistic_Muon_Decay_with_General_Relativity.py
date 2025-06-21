import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sqrt

# Parameters
h, v = 10000, 0.99 * 3e8  # height in meters, speed in m/s
c, tau = 3e8, 2.2e-6  # speed of light in m/s, muon lifetime in seconds
N0, G, M = 10000, 6.67430e-11, 5.972e24  # number of muons, gravitational constant, mass of Earth in kg
R = 6.371e6  # radius of Earth in meters

# GR time dilation factor
r = symbols('r')
phi = -G * M / r
gamma_GR = sqrt(1 - 2 * phi / (c**2))
gamma_GR_val = float(gamma_GR.subs(r, R + h).evalf())  # Convert to Python float

# Special Relativity time dilation factor
gamma_SR = 1 / sqrt(1 - (v / c)**2)

# Total time dilation factor
t_eff = h / v / (gamma_SR * gamma_GR_val)

# Decay
N_GR = N0 * np.exp(-t_eff / tau)
N_nonreal = N0 * np.exp(-h / v / tau)

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(['General Relativity', 'Special Relativity'], [N_GR, N_nonreal], color=['blue', 'orange'])
plt.title('Muon Decay: General Relativity vs Special Relativity')
plt.ylabel('Number of Muons Remaining')
plt.xlabel('Theory')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('muon_decay_comparison.png')
plt.show()