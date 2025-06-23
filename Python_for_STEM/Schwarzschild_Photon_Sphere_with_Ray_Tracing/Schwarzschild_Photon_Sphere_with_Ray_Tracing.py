import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parameters
M, G, c = 1.0, 6.67430e-11, 3e8
phi = np.linspace(0 ,10 * np.pi, 1000)
r_photon = 3 * M # Photon sphere radius

# Geodesic equation for null rays
def photon_orbit(y, phi, b):
    r , dr = y
    d2r = (r - 2 * M) * (b**2 / r**3 - 1 / (r - 2 * M))
    return [dr, d2r]

# Impact parameter for photon sphere
b = r_photon * np.sqrt(1 / (r_photon - 2 * M))

# Solve orbit
sol = odeint(photon_orbit, [5.0, 0], phi, args=(b,))

# Solve orbit
sol = odeint(photon_orbit, [5.0, 0], phi, args=(b,))
r = sol[:, 0]
x , y = r * np.cos(phi), r * np.sin(phi)

# Plot
plt.figure(figsize=(8, 8))
plt.plot(x, y, 'b-', label='Photon Orbit')
plt.plot(r_photon * np.cos(phi), r_photon * np.sin(phi), 'r--', label='Photon Sphere')
plt.title('Schwarzschild Photon Sphere with Ray Tracing')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()