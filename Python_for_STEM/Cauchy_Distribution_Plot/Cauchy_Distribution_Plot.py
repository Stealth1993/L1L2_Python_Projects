import numpy as np
import matplotlib.pyplot as plt

# Parameters for the Cauchy distribution
x0 = 0  # location parameter
gamma = 1  # scale parameter

# Generate x values
x = np.linspace(-10, 10, 1000)

# Calculate the Cauchy distribution PDF
def cauchy_pdf(x, x0, gamma):
    return 1 / (np.pi * gamma * (1 + ((x - x0) / gamma) ** 2))

# Calculate the PDF values
pdf_values = cauchy_pdf(x, x0, gamma)

# Plotting the Cauchy distribution
plt.figure(figsize=(10, 6))
plt.plot(x, pdf_values, label='Cauchy PDF', color='blue')
plt.title('Cauchy Distribution')
plt.xlabel('x')
plt.ylabel('Probability Density')
plt.axvline(x=x0, color='red', linestyle='--', label='Location Parameter (x0)')
plt.legend()
plt.grid()
plt.show()