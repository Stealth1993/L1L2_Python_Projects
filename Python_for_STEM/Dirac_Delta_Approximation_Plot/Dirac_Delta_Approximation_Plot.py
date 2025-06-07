import numpy as np
import matplotlib.pyplot as plt

# parameters
N = 1000  # number of points
x = np.linspace(-5, 5, N)  # x values
sigma = 0.1  # standard deviation for Gaussian approximation

# Gaussian function as an approximation of the Dirac delta function
def gaussian(x, sigma):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (x / sigma) ** 2)

# Calculate the Gaussian approximation
y = gaussian(x, sigma)

# Plotting the Gaussian approximation
plt.figure(figsize=(10, 6))
plt.plot(x, y, label=f'Gaussian Approximation (σ={sigma})', color='blue')
plt.title('Dirac Delta Function Approximation using Gaussian Function')
plt.xlabel('x')
plt.ylabel('Amplitude')
plt.axhline(0, color='black', lw=0.5, ls='--')
plt.axvline(0, color='black', lw=0.5, ls='--')
plt.xlim(-5, 5)
plt.ylim(-0.1, 1.5)
plt.grid()
plt.legend()
plt.show()

# This code generates a plot of the Gaussian function as an approximation of the Dirac delta function.
# The Gaussian function is centered at zero and has a small standard deviation (sigma).
# The plot illustrates how the Gaussian function approaches the Dirac delta function as sigma approaches zero.
# The plot shows the Gaussian function's peak at x=0, which represents the Dirac delta function's property of being infinitely high at zero and zero elsewhere.
# The code uses numpy for numerical calculations and matplotlib for plotting.

