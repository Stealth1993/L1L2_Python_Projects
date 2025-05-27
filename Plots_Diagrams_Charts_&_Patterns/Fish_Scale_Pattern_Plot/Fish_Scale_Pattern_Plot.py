import numpy as np
import matplotlib.pyplot as plt

rows, cols = 10, 10
radius = 0.5
def fish_scale_pattern(rows, cols, radius):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.axis('off')

    for i in range(rows):
        for j in range(cols):
            x = j * radius * 2
            y = i * radius * 2
            circle = plt.Circle((x, y), radius, color='blue', fill=False, linewidth=1.5)
            ax.add_artist(circle)

            if (i + j) % 2 == 0:
                scale = plt.Circle((x, y), radius * 0.5, color='blue', fill=True)
                ax.add_artist(scale)

    plt.xlim(-radius, cols * radius * 2)
    plt.ylim(-radius, rows * radius * 2)
    plt.title('Fish Scale Pattern')
    plt.show()

fish_scale_pattern(rows, cols, radius)
