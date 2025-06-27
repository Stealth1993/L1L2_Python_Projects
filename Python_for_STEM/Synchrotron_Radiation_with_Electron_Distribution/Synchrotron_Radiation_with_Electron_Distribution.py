import numpy as np
import matplotlib.pyplot as plt
from scipy.special import iv

# Parameters 
B = 1e-6 # Magnetic field
nu = np.longspace(8, 12, 100) # Frequency (Hz)
p = 2.5 # Power-low index
N0 = 1e5 # Normalization

# Synchrotron critical frequency and emissivity
def synchrotron_emissivity(nu, B, p):
    nu_c = 4.2e6 * B * (nu / 1e9)**(2 / (p + 1))
    x = nu / nu_c
    F = x**(1/3) * np.exp(-x)
    return N0 * B**((p +1 ) / 2) * F

# Spectrum
P_nu = synchrotron_emissivity(nu, B, p)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(nu, P_nu)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Spectral Power Density (W/Hz)')
plt.title('Synchrotron Radiation Spectrum')
plt.grid()
plt.show()