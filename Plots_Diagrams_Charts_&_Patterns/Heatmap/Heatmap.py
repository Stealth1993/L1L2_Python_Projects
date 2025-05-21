import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.cm as cm

# Sample data
data = np.random.rand(10, 12)
data = pd.DataFrame(data, columns=[f'Col {i}' for i in range(12)], index=[f'Row {i}' for i in range(10)])

# Create a mask for the upper triangle
mask = np.triu(np.ones_like(data, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(10, 8))

# Generate a custom colormap
cmap = cm.get_cmap('coolwarm', 10)
cmap.set_bad(color='lightgray')
cmap.set_under(color='lightgray')
cmap.set_over(color='darkred')
cmap.set_bad(color='lightgray')

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(data, mask=mask, cmap=cmap, cbar_kws={"shrink": .8}, ax=ax)
ax.set_title('Heatmap with Custom Colormap and Mask')
ax.set_xlabel('Columns')
ax.set_ylabel('Rows')

# Show the plot
plt.show()