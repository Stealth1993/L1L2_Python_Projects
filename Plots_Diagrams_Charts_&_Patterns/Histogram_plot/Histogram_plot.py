import numpy as np
import matplotlib.pyplot as plt

# Set a random seed for reproducibility
np.random.seed(0)

# Generate sample data: 1000 points from a standard normal distribution
data = np.random.normal(0, 1, 1000)

# Define 10 distinct colors using the 'tab10' colormap
colors = plt.get_cmap('tab10').colors

# Create the histogram with 10 bins and capture the patches
n, bins, patches = plt.hist(data, bins=10, edgecolor='black')

# Assign a different color to each bin
for i, patch in enumerate(patches):
    patch.set_facecolor(colors[i])

# Add titles and labels
plt.title('Histogram with 10 Bins and Different Colors')
plt.xlabel('Value')
plt.ylabel('Frequency')

# Save the plot to a file instead of displaying it
#plt.savefig('histogram.png')

# Display the plot
plt.show()