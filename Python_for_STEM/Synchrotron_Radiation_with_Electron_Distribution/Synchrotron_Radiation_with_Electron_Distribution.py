import numpy as np
import matplotlib.pyplot as plt
from scipy.special import iv

# Description: This program computes synchrotron radiation from a power-law electron distribution,
# integrating over the electron energy spectrum.

# Parameters
B = 1e-6  # Magnetic field (T)
nu = np.logspace(8, 12, 100)  # Frequency (Hz)
p = 2.5  # Power-law index
N0 = 1e5  # Normalization

# Synchrotron critical frequency and emissivity
def synchrotron_emissivity(nu, B, p):
    nu_c = 4.2e6 * B * (nu / 1e9)**(2 / (p + 1))
    x = nu / nu_c
    F = x**(1/3) * np.exp(-x)  # Approximation of synchrotron function
    return N0 * B**((p + 1) / 2) * F

# Spectrum
P_nu = synchrotron_emissivity(nu, B, p)

# Plot
plt.figure(figsize=(10, 6))
plt.loglog(nu, P_nu)
plt.title('Synchrotron Radiation from Power-Law Electron Distribution')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (arbitrary units)')
plt.grid(True)
plt.show()