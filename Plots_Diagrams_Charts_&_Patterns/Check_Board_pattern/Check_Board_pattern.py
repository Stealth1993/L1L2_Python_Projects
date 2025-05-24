import numpy as np
import matplotlib.pyplot as plt

def check_board_pattern(n, m):
    # Create a checkerboard pattern
    checkerboard = np.zeros((n, m))
    checkerboard[1::2, ::2] = 1
    checkerboard[::2, 1::2] = 1

# Plot the checkerboard pattern
    plt.imshow(checkerboard, cmap='gray', interpolation='nearest')
    plt.title(f'Checkerboard Pattern ({n}x{m})')
    plt.xticks([])
    plt.yticks([])
    plt.axis()
    plt.show()

if __name__ == "__main__":
    n = 8  # Number of rows
    m = 8  # Number of columns
    check_board_pattern(n, m)