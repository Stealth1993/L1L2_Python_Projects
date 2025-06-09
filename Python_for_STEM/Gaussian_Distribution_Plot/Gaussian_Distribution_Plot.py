import numpy as np
import matplotlib.pyplot as plt

# Description: This program generates a Gaussian distribution plot with specified parameters.
# This program is designed to visualize the Gaussian distribution, which is a fundamental concept in statistics and probability theory.
# It uses NumPy for numerical calculations and Matplotlib for plotting the distribution.

# Parameters for the Gaussian distribution
mu = 0.0  # Mean of the distribution
sigma = 1.0  # Standard deviation of the distribution

# Generate x values
x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)

# Calculate the Gaussian distribution
y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, label=f'Gaussian Distribution\n$\\mu={mu}, \\sigma={sigma}$', color='blue')
plt.title('Gaussian Distribution Plot')
plt.xlabel('x')
plt.ylabel('Probability Density')
plt.legend()
plt.grid()
plt.xlim(mu - 4*sigma, mu + 4*sigma)
plt.ylim(0, np.max(y) * 1.1)
plt.axvline(mu, color='red', linestyle='--', label='Mean ($\\mu$)')
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
plt.legend()
plt.show()