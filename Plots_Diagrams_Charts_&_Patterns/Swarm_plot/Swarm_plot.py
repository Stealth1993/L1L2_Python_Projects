import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Dummy data
np.random.seed(0)
n_samples = 100
data = pd.DataFrame({
    'x': np.random.rand(n_samples),
    'y': np.random.rand(n_samples),
    'hue': np.random.choice(['A', 'B', 'C'], n_samples)
})

# Bin the 'x' values into 10 bins
bins = np.linspace(0, 1, 11)  # Creates 10 equal-width bins from 0 to 1
data['x_bin'] = pd.cut(data['x'], bins=bins)

# Create a swarm plot with binned 'x'
plt.figure(figsize=(12, 6))
sns.swarmplot(x='x_bin', y='y', hue='hue', data=data, dodge=True, palette='Set2')
plt.title('Swarm Plot with Binned X-axis')
plt.xlabel('X-axis (Binned)')
plt.ylabel('Y-axis')
plt.legend(title='Hue')

# Rotate x-tick labels for better readability
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
# This code creates a swarm plot using seaborn with the x-axis values binned into 10 equal-width bins.
# The y-axis represents the original 'y' values, and the hue represents different categories.