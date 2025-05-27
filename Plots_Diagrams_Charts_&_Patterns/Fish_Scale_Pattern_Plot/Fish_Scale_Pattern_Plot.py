import numpy as np
import matplotlib.pyplot as plt

rows, cols = 10, 10
radius = 0.5

fig, ax = plt.subplots(figsize=(8, 8))

ax.set_xlim(0, cols * radius)
ax.set_ylim(0, (rows + 1) * (radius / 2))
ax.set_aspect('equal')
ax.axis('off')
colors = ['#FF5733', '#33FF57', '#3357FF', '#F0E68C', '#FF69B4']

# Create the fish scale pattern
for row in range(rows):
    for col in range(cols):
        x = col * radius
        y = row * (radius / 2)
        if row % 2 == 0:
            x += radius / 2
        semicircle = plt.Circle((x, y), radius, color=np.random.choice(colors), alpha=0.7, edgecolor='black')
        ax.add_artist(semicircle)

# Show the plot
plt.title('Fish Scale Pattern Plot')
plt.show()