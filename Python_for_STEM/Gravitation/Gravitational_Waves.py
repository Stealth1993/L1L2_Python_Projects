import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.constants import c, G

# Parameters for the binary black hole system
mass1 = 30 * u.M_sun  # Mass of the first black hole
mass2 = 30 * u.M_sun  # Mass of the second black hole
distance = 400 * u.Mpc  # Distance to the binary system
frequency = np.linspace(10, 1000, 1000) * u.Hz  # Frequency range for the waveform
t = np.linspace(0, 1, 1000) * u.s  # Time array for the waveform

# Calculate the chirp mass
chirp_mass = (mass1 * mass2)**(3/5) / (mass1 + mass2)**(1/5)

# Calculate the strain of the gravitational wave
def strain(t, chirp_mass, distance):
    """Calculate the strain of the gravitational wave."""
    h0 = (4 * G * chirp_mass / (c**2 * distance)).to(u.dimensionless_unscaled)
    return h0 * np.sin(2 * np.pi * frequency * t * u.radian)

# Generate the waveform
waveform = strain(t, chirp_mass, distance)

# Plot the gravitational wave strain
plt.figure(figsize=(10, 6))
plt.plot(t, waveform, label='Gravitational Wave Strain')
plt.title('Gravitational Wave Strain from Binary Black Hole Merger')
plt.xlabel('Time (s)')
plt.ylabel('Strain')
plt.legend()
plt.grid()
plt.show()