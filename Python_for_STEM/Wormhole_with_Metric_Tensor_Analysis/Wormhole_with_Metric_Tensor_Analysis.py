import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Matrix

# Parameters
l, phi = np.linspace(0, 10, 100), np.linspace(0, 2 * np.pi, 100)
L, PHI = np.meshgrid(l, phi)
b0 = 1.0 # throat radius

# Embedding function
z = np.sqrt(L**2 + b0**2) * np.exp(1j * PHI + np.pi / 2
                                   )  # Wormhole throat in complex plane    
# Metric tensor components
def metric_tensor(L, PHI, b0):
    g_tt = -1
    g_rr = (L**2 + b0**2) / (L**2)
    g_pp = (L**2 + b0**2) * L**2
    g_zz = 1
    return Matrix([[g_tt, 0, 0, 0],
                   [0, g_rr, 0, 0],
                   [0, 0, g_pp, 0],
                   [0, 0, 0, g_zz]])

# Calculate the metric tensor
G = metric_tensor(L, PHI, b0)
# Calculate the determinant of the metric tensor
det_G = G.det()
# Calculate the inverse of the metric tensor
G_inv = G.inv()
# Calculate the Christoffel symbols
def christoffel_symbols(G):
    gamma = np.zeros((4, 4, 4))
    for i in range(4):
        for j in range(4):
            for k in range(4):
                gamma[i, j, k] = 1/2 * sum(G_inv[i, l] * (G[l, j, k] + G[l, k, j] - G[j, k, l]) for l in range(4))
    return gamma
gamma = christoffel_symbols(G)
# Calculate the Riemann curvature tensor
def riemann_curvature_tensor(G, gamma):
    R = np.zeros((4, 4, 4, 4))
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    R[i, j, k, l] = (gamma[i, j, k].diff(l) - gamma[i, j, l].diff(k) +
                                     sum(gamma[i, m, k] * gamma[m, j, l] - gamma[i, m, l] * gamma[m, j, k]
                                         for m in range(4)))
    return R
R = riemann_curvature_tensor(G, gamma)

# Plotting the wormhole
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(np.real(z), np.imag(z), np.abs(z), cmap='inferno')
ax.set_xlabel('Real Part')
ax.set_ylabel('Imaginary Part')
ax.set_zlabel('Magnitude')
ax.set_title('Wormhole Visualization with Metric Tensor Analysis')
plt.show()