import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from sympy import symbols, diff, solve

# Parameters
M = 10.0  # Mass of the lensing object (in solar masses)
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
c = 3e8  # Speed of light (m/s)
D_L = 1e22  # Distance to lensing object (in meters)
D_S = 2e22  # Distance to source (in meters)
theta_E = np.sqrt((4 * G * M * 1.9e30) / (D_L * D_S) / (c**2 * D_L * D_S))  # Einstein radius

# Symbolic Lens Equation
def lens_equation(y, M, D_L, D_S):
    G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
    c = 299792458  # Speed of light (m/s)
    y_lens = symbols('y_lens')
    deflection_angle = (4 * G * M) / (c**2 * D_L * y_lens)
    return y - y_lens + deflection_angle

# Solve the lens equation for the source position
def solve_lens_equation(y_source, M, D_L, D_S):
    y_lens = symbols('y_lens')
    equation = lens_equation(y_lens, M, D_L, D_S)
    solution = fsolve(lambda y: equation.subs(y_lens, y), y_source)
    return solution

# Create a grid of points
x = np.linspace(-2e21, 2e21, 100)
y = np.linspace(-2e21, 2e21, 100)
X, Y = np.meshgrid(x, y)

# Calculate deflection angles and lensed positions
deflection = np.zeros(X.shape + (2,))  # Shape (100, 100, 2)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        y_point = np.array([X[i, j], Y[i, j]])
        deflection_angle = (4 * G * M) / (c**2 * D_L * np.linalg.norm(y_point))
        deflection[i, j] = y_point - deflection_angle

# Calculate magnification
def calculate_magnification(deflection):
    magnification = np.zeros(deflection.shape[:2])
    for i in range(deflection.shape[0]):
        for j in range(deflection.shape[1]):
            y_lens = np.linalg.norm(deflection[i, j])
            if y_lens != 0:
                magnification[i, j] = 1 / (1 - (theta_E**2 / y_lens**2))
            else:
                magnification[i, j] = np.inf  # Infinite magnification at the lens center
    return magnification

# Calculate magnification
magnification = calculate_magnification(deflection)

# Plotting the results
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(magnification, extent=(-2e21, 2e21, -2e21, 2e21), origin='lower', cmap='hot')
plt.colorbar(label='Magnification')
plt.title('Gravitational Lensing Magnification')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.subplot(1, 2, 2)
plt.imshow(np.sqrt(deflection[..., 0]**2 + deflection[..., 1]**2), extent=(-2e21, 2e21, -2e21, 2e21), origin='lower', cmap='cool')
plt.colorbar(label='Deflection Angle (rad)')
plt.title('Gravitational Lensing Deflection Angle')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.tight_layout()
plt.show()