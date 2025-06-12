import numpy as np
import matplotlib.pyplot as plt

# Parameters
M = 1.0  # Mass of the lensing object (in solar masses)
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
D_L = 1e22 # Distance to lensing object (in meters)
D_S = 2e22 # Distance to source (in meters)
c = 3e8  # Speed of light (m/s)
y_source = np.array([0.0, 1e21])  # Position of the source (in meters)

# Einstein radius calculation
theta_E = np.sqrt((4 * G * M) * 1.9e30 / (D_L * D_S) / (c**2 * D_L * D_S))

# Deflection angle calculation
def deflection_angle(y, M, D_L, D_S):
    G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
    c = 299792458  # Speed of light (m/s)
    return (4 * G * M) / (c**2 * D_L * np.linalg.norm(y))

# Create a grid of points
x = np.linspace(-2e21, 2e21, 100)
y = np.linspace(-2e21, 2e21, 100)
X, Y = np.meshgrid(x, y)

# Calculate deflection angles
deflection = np.zeros(X.shape + (2,))  # Shape (100, 100, 2)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        y_point = np.array([X[i, j], Y[i, j]])
        deflection[i, j] = deflection_angle(y_point, M, D_L, D_S)

# Calculate the lensed positions
lensed_positions = np.zeros(X.shape + (2,))
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        y_point = np.array([X[i, j], Y[i, j]])
        lensed_positions[i, j] = y_point - deflection[i, j]

# Plotting the results
plt.figure(figsize=(10, 10))
plt.quiver(X, Y, deflection[..., 0], deflection[..., 1], color='blue', alpha=0.5)
plt.scatter(y_source[0], y_source[1], color='red', label='Source Position', s=100)
plt.scatter(lensed_positions[..., 0], lensed_positions[..., 1], color='green', label='Lensed Positions', s=1)
plt.title('Gravitational Lensing Simulation')
plt.xlabel('X Position (m)')
plt.ylabel('Y Position (m)')
plt.legend()
plt.grid()
plt.show()