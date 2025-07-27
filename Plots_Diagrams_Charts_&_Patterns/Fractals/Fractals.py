import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(c, max_iter=100):
    """Calculate Mandelbrot set membership"""
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def julia_set(z, c, max_iter=100):
    """Calculate Julia set membership"""
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

# Create complex plane for Mandelbrot
width, height = 800, 600
x_min, x_max = -2.5, 1.0
y_min, y_max = -1.25, 1.25

# Generate Mandelbrot set
mandelbrot_set = np.zeros((height, width))
for i in range(height):
    for j in range(width):
        c = complex(x_min + (x_max - x_min) * j / width,
                   y_min + (y_max - y_min) * i / height)
        mandelbrot_set[i, j] = mandelbrot(c)

# Generate Julia set
julia_c = complex(-0.7, 0.27015)  # Interesting Julia set parameter
julia_set_data = np.zeros((height, width))
x_min_j, x_max_j = -2, 2
y_min_j, y_max_j = -2, 2

for i in range(height):
    for j in range(width):
        z = complex(x_min_j + (x_max_j - x_min_j) * j / width,
                   y_min_j + (y_max_j - y_min_j) * i / height)
        julia_set_data[i, j] = julia_set(z, julia_c)

# Plot fractals
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

# Mandelbrot set
im1 = ax1.imshow(mandelbrot_set, extent=[x_min, x_max, y_min, y_max],
                cmap='hot', origin='lower')
ax1.set_title('Mandelbrot Set')
ax1.set_xlabel('Real')
ax1.set_ylabel('Imaginary')
plt.colorbar(im1, ax=ax1)

# Julia set
im2 = ax2.imshow(julia_set_data, extent=[x_min_j, x_max_j, y_min_j, y_max_j],
                cmap='viridis', origin='lower')
ax2.set_title(f'Julia Set (c = {julia_c})')
ax2.set_xlabel('Real')
ax2.set_ylabel('Imaginary')
plt.colorbar(im2, ax=ax2)

plt.tight_layout()
plt.show()