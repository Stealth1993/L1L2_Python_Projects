import numpy as np
import matplotlib.pyplot as plt

# Parameters
gamma = 10  # Lorentz factor
theta = np.linspace(0, np.pi / 2, 100)  # Angle from the jet axis

# Calculate the Doppler factor
def doppler_factor(gamma, theta):
    return gamma * (1 - np.cos(theta))
# Calculate the intensity of the jet
def jet_intensity(gamma, theta):
    return (gamma**2 * np.sin(theta)**2) / (1 + gamma**2 * (1 - np.cos(theta))**2)

# Calculate the Doppler factor and intensity
doppler = doppler_factor(gamma, theta)
intensity = jet_intensity(gamma, theta)

# Plotting the results
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(theta, doppler, label='Doppler Factor', color='blue')
plt.title('Doppler Factor vs Angle')
plt.xlabel('Angle (radians)')
plt.ylabel('Doppler Factor')
plt.grid()
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(theta, intensity, label='Jet Intensity', color='red')
plt.title('Jet Intensity vs Angle')
plt.xlabel('Angle (radians)')
plt.ylabel('Jet Intensity')
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

# This code simulates the relativistic jet with Lorentz invariance, calculating the Doppler factor and jet intensity as functions of angle from the jet axis.
# The results are visualized in two plots: one for the Doppler factor and another for the jet intensity.
