import numpy as np
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM
from sympy import symbols, Function, Matrix, simplify

# Define the cosmological parameters
H0 = 70  # Hubble constant in km/s/Mpc
cosmo = FlatLambdaCDM(H0=H0, Om0=0.3) 
# Define the redshift range
z = np.linspace(0, 2, 100)
d_L = cosmo.luminosity_distance(z).value  # Luminosity distance in Mpc

# tensor perturbations

h_ij = 0.01 * np.sin(z)
v = cosmo.H0.value * d_L * (1 + z + h_ij) / (1 + z)

# Plot the Hubble diagram
plt.figure(figsize=(10, 6))
plt.plot(d_L, v, 'o', label='Observed Velocities with Tensor Perturbations', markersize=3)
plt.plot(d_L, cosmo.H0.value * d_L, 'r-', label=f'H₀ = {H0} km/s/Mpc')
plt.title('Hubble Diagram with Tensor Perturbations')
plt.xlabel('Luminosity Distance (Mpc)')
plt.ylabel('Velocity (km/s)')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.xlim(1, 1000)
plt.ylim(1, 10000)
plt.show()