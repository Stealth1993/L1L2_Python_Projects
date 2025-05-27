import numpy as np
import matplotlib.pyplot as plt

rows, cols = 10, 10
radius = 0.5

fig, ax = plt.subplots(figsize=(8, 8))
for i in range(rows):
    for j in range(cols):
        # Calculate the center of each square
        center_x = j + 0.5
        center_y = i + 0.5
        
        # Create a circle at the center of each square
        circle = plt.Circle((center_x, center_y), radius, color='blue', alpha=0.5)
        
        # Add the circle to the plot
        ax.add_artist(circle)


# Set the limits and aspect of the plot
ax.set_xlim(0, cols)
ax.set_ylim(0, rows)
ax.set_aspect('equal')

# Hide the axes
ax.axis('off')

# Show the plot
plt.title('Fish Scale Pattern Plot')
plt.show()