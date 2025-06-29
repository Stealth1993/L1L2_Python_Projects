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

# This code generates a log-log plot of the synchrotron radiation spectrum using a simple approximation.y
# F(v/v_c) = (v/v_c)^(1/3) * exp(-v/v_c)y
# The frequency range is logarithmically spaced from 1 to 100,000.

# Application:
# This code can be used in astrophysics to visualize the synchrotron radiation spectrum emitted by relativistic electrons in magnetic fields.