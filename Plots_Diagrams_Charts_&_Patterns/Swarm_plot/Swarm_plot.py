import matplotlib.pyplot as plt
import seaborn as sns

#dummy data
import pandas as pd
import numpy as np

np.random.seed(0)
n_samples = 100
data = pd.DataFrame({
    'x': np.random.rand(n_samples),
    'y': np.random.rand(n_samples),
    'hue': np.random.choice(['A', 'B', 'C'], n_samples)
})

# Create a swarm plot
plt.figure(figsize=(10, 6))
sns.swarmplot(x='x', y='y', hue='hue', data=data, dodge=True, palette='Set2')
plt.title('Swarm Plot Example')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend(title='Hue')
plt.show()