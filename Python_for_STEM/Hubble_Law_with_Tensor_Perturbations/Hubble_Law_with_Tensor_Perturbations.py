import numpy as np
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM
from sympy import symbols, Matrix

# Description: This program simulates the Hubble law with tensor perturbations in a flat
# ΛCDM universe, incorporating metric fluctuations.

# Parameters
cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
z = np.linspace(0, 2, 100)
d_L = cosmo.luminosity_distance(z).value

# Tensor perturbation (simplified)
h_ij = 0.01 * np.sin(z)  # Metric perturbation
v = cosmo.H0.value * d_L * (1 + z + h_ij) / (1 + z)

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(d_L, v, label='Hubble Law with Tensor Perturbations', color='blue')
plt.title('Hubble Law with Tensor Perturbations')
plt.xlabel('Luminosity Distance (Mpc)')
plt.ylabel('Velocity (km/s)')
plt.grid()
plt.legend()
plt.show()