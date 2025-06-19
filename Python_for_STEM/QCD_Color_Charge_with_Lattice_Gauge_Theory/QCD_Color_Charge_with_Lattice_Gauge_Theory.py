# this program is a simple example of how to use the QCD_Color_Charge_with_Lattice_Gauge_Theory module
# it will create a lattice gauge theory and calculate the color charge of a quark
import numpy as np
import matplotlib.pyplot as plt

# Parameters
lattice_size = 10  # Size of the lattice
x, y = np.meshgrid(np.arange(lattice_size), np.arange(lattice_size))
phi = np.random.rand(lattice_size, lattice_size) * 2 * np.pi  # Random phase field
gauge_field = np.exp(1j * phi)  # Gauge field as complex exponentials

# Action (simplified plaquette action)
def action(gauge_field):
    plaquette = np.mean(np.abs(gauge_field)**2)  # Simplified action
    return plaquette

# Calculate the action
plaquette_action = action(gauge_field)
print(f"Plaquette action: {plaquette_action}")

# Visualize the gauge field
plt.figure(figsize=(8, 8))
plt.quiver(x, y, np.real(gauge_field), np.imag(gauge_field),
              color='blue', scale=5, headlength=4)
plt.title('Gauge Field Visualization')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(-0.5, lattice_size - 0.5)
plt.ylim(-0.5, lattice_size - 0.5)
plt.grid()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
