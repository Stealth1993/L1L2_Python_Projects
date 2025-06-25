import numpy as np
import matplotlib.pyplot as plt
from scipy.special import voigt_profile


# Parameters
lambda_0 = 500e-9 # central wavelength(m)
T = 6000 # Temperature(K)
k_B = 1.380649e-23 # Boltzmann constant (J/K)
m = 1.673e-27 # Mass of Hydrogen atom (kg)
c = 3e8 # Speed of light (m/s)
gamma = 1e7 # Lorentzian width (Hz)

# Wavelength grid
lambda_vals = np.linspace(499e-9, 501e-9, 1000)
nu = c / lambda_vals
nu_0 = c / lambda_0

# Doppler width
sigma = nu_0 * np.sqrt(k_B * T / (m * c**2))

# Voigt profile
profile = voigt_profile(nu - nu_0, sigma, gamma)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(lambda_vals * 1e9, 1 - profile / profile.max(), 'b-')
plt.title('Steller Spectrum with Doppler Broadening')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized Intensity')
plt.grid()
plt.show()