import numpy as np
import matplotlib.pyplot as plt

# Parameters
nu = np.logspace(0, 5, 1000) # Frequency range
nu_c = 1e3 # Critical frequenc

# Synchrotron spectrum (approximation)
F = (nu / nu_c)**(1/3) * np.exp(-nu / nu_c)

# Plot
plt.loglog(nu, F)
plt.title('Synchrotron Radiation Spectrum')
plt.xlabel('Frequency (V)')
plt.ylabel('Power (F(v/v_c))')
plt.grid(True, which='both')
plt.show()