import numpy as np
import matplotlib.pyplot as plt

#Parameters for the Breit-Wigner distribution
E = np.linspace(0,200,1000)
E0 = 100  # Resonance energy
Gamma = 10  # Width of the resonance

#Breit-Wigner formula
f = (Gamma / (2 * np.pi)) / ((E - E0)**2 + (Gamma / 2)**2)

#plot
plt.plot(E, f)
plt.title('Breit-Wigner Distribution')
plt.xlabel('Energy (E)')
plt.ylabel('Cross Section (f)')
plt.grid(True)
plt.xlim(0, 200)
plt.ylim(0, 0.1)
plt.show()