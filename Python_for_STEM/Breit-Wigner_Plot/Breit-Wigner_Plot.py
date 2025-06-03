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
plt.axvline(E0, color='r', linestyle='--', label='Resonance Energy (E0)')
plt.legend()
plt.show()

# This code generates a plot of the Breit-Wigner distribution, which is commonly used in particle physics to describe the behavior of resonances. The plot shows how the cross section varies with energy around the resonance energy E0, with a width defined by Gamma. The vertical dashed line indicates the position of the resonance energy.
# The x-axis represents the energy (E) and the y-axis represents the cross section (f).
# The plot is generated using Matplotlib, a popular plotting library in Python.

# This code is applicable in the context of particle physics, particularly in the study of resonances in scattering processes. The Breit-Wigner distribution is a fundamental concept used to describe the probability of finding a particle at a certain energy level, especially near resonance conditions. It is widely used in experimental and theoretical physics to analyze data from particle collisions and decays.
# The parameters E0 and Gamma can be adjusted to model different resonances, making this code versatile for various applications in particle physics research.