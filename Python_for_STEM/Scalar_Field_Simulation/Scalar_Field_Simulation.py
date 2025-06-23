import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft2, ifft2

# Parameters
N = 64 # Grid Size
L = 10.0 # Box Size
dt = 0.01 # Time step
m = 1.0 # Mass

# Grid
x = np.linspace(-L/2, L/2, N, endpoint=False)
kx = 2 * np.pi * np.fft.fftfreq(N, L/N)
kx, ky = np.meshgrid(kx, kx)

# Initial condition: Gaussian pulse
phi = np.exp(-(x[:, None]**2 + x[None, :]**2) /2)
pi = np.zeros((N, N)) # Momentum

# Dispersion relation
omega = np.sqrt(kx**2 + ky**2 + m**2)

# Time evolution in Fourier space
def evolve (phi, pi, t):
    phi_k = fft2(phi)
    pi_k = fft2(pi)
    phi_k_new = phi_k * np.cos(omega * t) + pi_k * np.sin(omega * t) / omega
    pi_k_new = -phi_k * omega * np.sin(omega * t) + pi_k * omega * np.cos(omega * t)
    return ifft2(phi_k_new).real, ifft2(pi_k_new).real

# Simulate and plot
plt.figure(figsize=(10, 8))
for i in range(5):
    phi, pi = evolve(phi, pi, dt * 10)
    plt.clf()
    plt.imshow(phi, extent=[-L/2, L/2, -L/2, L/2], cmap='viridis')
    plt.title(f'Scalar Field at t={i*0.1:.1f}')
    plt.colorbar(label='φ')
plt.show()