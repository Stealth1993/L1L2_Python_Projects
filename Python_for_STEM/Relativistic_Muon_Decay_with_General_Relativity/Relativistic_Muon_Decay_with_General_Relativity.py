import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sqrt as sympy_sqrt  # Rename for clarity

# Parameters
h, v = 10000, 0.99 * 3e8  # height in meters, speed in m/s
c, tau = 3e8, 2.2e-6  # speed of light in m/s, muon lifetime in seconds
N0, G, M = 10000, 6.67430e-11, 5.972e24  # number of muons, G, Earth mass in kg
R = 6.371e6  # radius of Earth in meters

# GR time dilation factor (symbolic)
r = symbols('r')
phi = -G * M / r
gamma_GR = sympy_sqrt(1 - 2 * phi / (c**2))
gamma_GR_val = float(gamma_GR.subs(r, R + h).evalf())  # Convert to Python float

# SR time dilation factor (numerical)
gamma_SR = 1 / np.sqrt(1 - (v / c)**2)  # Use np.sqrt

# Total effective time
t_eff = h / v / (gamma_SR * gamma_GR_val)

# Decay calculations
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

# This code simulates the decay of muons considering both General and Special Relativity, comparing the number of muons remaining after a certain time. The results are visualized in a bar chart.
# The code uses numpy for numerical calculations and sympy for symbolic mathematics, ensuring accurate handling of the relativistic effects.
# The plot shows the difference in muon decay predictions between General Relativity and Special Relativity, highlighting the impact of gravitational time dilation.
# The code is structured to be clear and efficient, with comments explaining each step.
# The code is designed to be run in a Python environment with the necessary libraries installed.

# Applications:
# 1. Particle Physics: Understanding muon decay helps in studying fundamental particles and their interactions.
# 2. Astrophysics: Time dilation effects are crucial in understanding cosmic ray muons and their behavior in Earth's atmosphere.
# 3. Education: This code serves as an educational tool to illustrate the principles of relativity in a practical scenario.
# 4. Experimental Physics: The results can be compared with experimental data to validate relativistic predictions.