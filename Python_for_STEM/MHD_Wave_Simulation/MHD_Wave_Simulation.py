import numpy as np
import matplotlib.pyplot as plt

# Parameters
nx = 1000  # Number of spatial points
dx = 0.1  # Spatial step size
dt = 0.01  # Time step size
B0 = 1.0  # Initial magnetic field strength
vA = 1.0  # Alfvén speed

# Initial conditions
x = np.linspace(0, (nx - 1) * dx, nx)
v = np.sin(2 * np.pi * x / (nx * dx))  # Initial velocity profile
B = B0 + 0.1 * np.sin(2 * np.pi * x / (nx * dx))  # Initial magnetic field profile

# Time evolution
def update_wave(v, B, dt, dx, vA):
    # Update velocity and magnetic field using finite difference method
    dv = -vA * np.gradient(B, dx) * dt
    dB = -vA * np.gradient(v, dx) * dt
    v += dv
    B += dB
    return v, B

# Time loop
for t in np.arange(0, 1, dt):
    v, B = update_wave(v, B, dt, dx, vA)

# Plotting the results
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(x, v, label='Velocity (v)', color='blue')
plt.title('MHD Wave Simulation: Velocity Profile')
plt.xlabel('Position (x)')
plt.ylabel('Velocity (v)')
plt.grid(True)
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(x, B, label='Magnetic Field (B)', color='red')
plt.title('MHD Wave Simulation: Magnetic Field Profile')
plt.xlabel('Position (x)')
plt.ylabel('Magnetic Field (B)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# This code simulates the propagation of magnetohydrodynamic (MHD) waves in a plasma.
# It initializes a velocity profile and a magnetic field profile, then updates them over time.
# The results are plotted to visualize the wave propagation in both the velocity and magnetic field profiles.
# The simulation uses a simple finite difference method to update the wave profiles.
# The parameters can be adjusted to explore different wave behaviors.
# The simulation is a basic representation and can be extended with more complex initial conditions or boundary conditions.


# Note: This code is a simplified simulation and does not include all physical effects present in real MHD systems.
# It serves as a basic example of how to simulate MHD waves using numerical methods.

# Application:
# This code can be used in educational settings to demonstrate the principles of magnetohydrodynamics (MHD) and wave propagation in plasmas.