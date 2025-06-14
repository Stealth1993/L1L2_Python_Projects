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
def tensor_perturbations(z):
    """Calculate tensor perturbations as a function of redshift."""
    # Placeholder for actual tensor perturbation calculation
    # Here we assume a simple model where perturbations decrease with redshift
    return 0.1 * (1 + z)**(-2)

# Calculate the tensor perturbations
perturbations = tensor_perturbations(z)
# Calculate the observed velocities
velocities = H0 * d_L + perturbations
# Plot the Hubble diagram
plt.figure(figsize=(10, 6))
plt.scatter(d_L, velocities, c='blue', label='Observed Velocities')
plt.plot(d_L, H0 * d_L, 'r-', label=f'H₀ = {H0} km/s/Mpc')
plt.title('Hubble Diagram with Tensor Perturbations')
plt.xlabel('Luminosity Distance (Mpc)')
plt.ylabel('Velocity (km/s)')
plt.legend()
plt.grid(True)
plt.show()
