import matplotlib.pyplot as plt
import numpy as np

categories = ['Speed', 'Reliability', 'Comfort', 'Safety', 'Efficiency']
values = [4, 3, 5, 2, 4]

# Number of variables
N = len(categories)
angle = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
values += values[:1]  # Repeat the first value to close the circle
angle += angle[:1]  # Repeat the first angle to close the circle

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.fill(angle, values, color='red', alpha=0.25)
ax.set_yticklabels([])  # Hide the radial ticks
ax.set_xticks(angle[:-1])  # Set the angular ticks
ax.set_xticklabels(categories)  # Set the category labels
ax.set_title('Spider Chart Example', size=20, color='blue', weight='bold')
ax.grid(True)  # Show the grid
plt.show()