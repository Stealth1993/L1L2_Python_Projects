import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

def riemann_sum(func, a, b, n, method='midpoint'):
    """Calculate Riemann sum approximation"""
    dx = (b - a) / n
    if method == 'left':
        x = a
        total = sum(func(x + i * dx) for i in range(n))
    elif method == 'right':
        x = b
        total = sum(func(x - i * dx) for i in range(n))
    else:  # midpoint
        total = sum(func(a + (i + 0.5) * dx) for i in range(n))
    return total * dx

# Plot Riemann sums
x = np.linspace(0, 1, 100)
y = np.sin(x)

plt.plot(x, y, label='sin(x)')
for method in ['left', 'right', 'midpoint']:
    approx = riemann_sum(np.sin, 0, 1, 10, method=method)
    plt.axhline(y=approx, color='r', linestyle='--', label=f'{method} Riemann sum')

plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Riemann Sum Approximations')
plt.show()