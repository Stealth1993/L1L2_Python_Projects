import numpy as np
import matplotlib.pyplot as plt

# Generate sample data: 1000 random numbers from a normal distribution

data = np.random.randn(1000)
# Create a histogram
plt.hist(data, bins=30, alpha=0.5, color='b')
plt.title('Histogram of Random Data')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()