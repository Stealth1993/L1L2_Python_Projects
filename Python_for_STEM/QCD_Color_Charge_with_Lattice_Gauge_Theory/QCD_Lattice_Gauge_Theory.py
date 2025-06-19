import numpy as np
import matplotlib.pyplot as plt

# Description: This program simulates a simplified U(1) lattice gauge theory as an
# approximation to QCD color charge interactions.

# Parameters
L = 10  # Lattice size
x, y = np.meshgrid(np.arange(L), np.arange(L))
phi = np.random.uniform(0, 2 * np.pi, (L, L))  # Gauge field

# Action (simplified plaquette)
plaquette = np.cos(phi - np.roll(phi, 1, axis=0) - np.roll(phi, 1, axis=1) + np.roll(np.roll(phi, 1, axis=0), 1, axis=1))

# Plot
plt.figure(figsize=(10, 6))
plt.imshow(plaquette, cmap='viridis')
plt.title('QCD Lattice Gauge Theory (Simplified U(1))')
plt.colorbar(label='Plaquette Value')
plt.show()