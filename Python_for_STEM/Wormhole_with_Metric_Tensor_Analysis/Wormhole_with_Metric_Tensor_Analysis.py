import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Matrix, simplify, diff, lambdify

# Symbolic variables
r, phi = symbols('r phi', real=True)
b0 = symbols('b0', real=True, positive=True)  # Throat radius as a symbol

# Metric tensor components (symbolic)
g_tt = -1
g_rr = (r**2 + b0**2) / (r**2 + 1e-10)  # Avoid divide by zero with small offset
g_pp = (r**2 + b0**2) * r**2
g_zz = 1

# Define metric tensor symbolically
def metric_tensor(r, phi, b0):
    return Matrix([[g_tt, 0, 0, 0],
                   [0, g_rr, 0, 0],
                   [0, 0, g_pp, 0],
                   [0, 0, 0, g_zz]])

# Calculate metric tensor
G_sym = metric_tensor(r, phi, b0)

# Determinant and inverse (symbolic)
det_G_sym = G_sym.det()
G_inv_sym = G_sym.inv()

# Numerical evaluation setup
r_vals, phi_vals = np.linspace(0.1, 10, 100), np.linspace(0, 2 * np.pi, 100)  # Start from 0.1 to avoid r=0
R, PHI = np.meshgrid(r_vals, phi_vals)
b0_val = 1.0

# Lambdify for numerical evaluation
g_rr_func = lambdify((r, b0), g_rr, "numpy")
g_pp_func = lambdify((r, b0), g_pp, "numpy")

# Numerical metric components
g_rr_num = g_rr_func(R, b0_val)
g_pp_num = g_pp_func(R, b0_val)

# Wormhole embedding (numerical for plotting)
z = np.sqrt(R**2 + b0_val**2) * np.exp(1j * PHI + np.pi / 2)

# Plotting the wormhole
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(np.real(z), np.imag(z), np.abs(z), cmap='inferno')
ax.set_xlabel('Real Part')
ax.set_ylabel('Imaginary Part')
ax.set_zlabel('Magnitude')
ax.set_title('Wormhole Visualization with Metric Tensor Analysis')
plt.show()