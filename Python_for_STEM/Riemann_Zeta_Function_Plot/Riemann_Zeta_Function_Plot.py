import numpy as np
import matplotlib.pyplot as plt
from scipy.special import zeta

# Parameters
t = np.linspace(0, 50, 1000) # Imaginary part range
s = 0.5 + 1j * t # Critical line: Re(s) = 0.5

# Compute Zeta Function
zeta_vals = zeta(s)
real_part = np.real(zeta_vals)
imag_part = np.imag(zeta_vals)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(t, real_part, label='Real Part')
plt.plot(t, imag_part, label='Imaginary Part')
plt.title('Riemann Zeta Function along Critical Line (Re(s) = 0.5)')
plt.xlabel('Imaginary Part (t)')
plt.ylabel('ζ(0.5 + it)')
plt.legend()
plt.grid(True)
plt.show()