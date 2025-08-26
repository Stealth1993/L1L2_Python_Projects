import numpy as np
import matplotlib.pyplot as plt 
from scipy import integrate

def riemann_sum(func, a, b, n, method='midpoint'):
    """Calculate Riemann sum approximation"""
    dx = (b - a) / n
    x = np.linspace(a, b, n+1)
    
    if method == 'left':
        x_sample = x[:-1]
    elif method == 'right':
        x_sample = x[1:]
    elif method == 'midpoint':
        x_sample = (x[:-1] + x[1:]) / 2
    
    y_sample = func(x_sample)
    return np.sum(y_sample * dx), x_sample, y_sample, dx

# Define function
def f(x):
    return x**2 * np.sin(x) + 1

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Calculus Visualization Suite', fontsize=16)

x = np.linspace(0, 2*np.pi, 1000)
y = f(x)

# Integration approximation
a, b = np.pi/2, 3*np.pi/2
for i, (n, ax) in enumerate(zip([5, 10, 20, 50], axes.flat)):
    ax.plot(x, y, 'b-', linewidth=2, label='f(x) = x²sin(x) + 1')
    
    # Calculate Riemann sum
    approx, x_sample, y_sample, dx = riemann_sum(f, a, b, n)
    
    # Draw rectangles
    for xs, ys in zip(x_sample, y_sample):
        ax.bar(xs, ys, width=dx, alpha=0.3, color='red', align='center',
               edgecolor='black')
    
    # Exact integral
    exact, _ = integrate.quad(f, a, b)
    
    ax.axvline(x=a, color='green', linestyle='--', alpha=0.7)
    ax.axvline(x=b, color='green', linestyle='--', alpha=0.7)
    ax.set_title(f'n={n}, Approx={approx:.3f}, Exact={exact:.3f}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 2*np.pi)

plt.tight_layout()
plt.show()

# Show convergence
n_values = np.logspace(1, 3, 20).astype(int)
approximations = []
exact, _ = integrate.quad(f, a, b)

for n in n_values:
    approx, _, _, _ = riemann_sum(f, a, b, n)
    approximations.append(approx)

plt.figure(figsize=(10, 6))
plt.semilogx(n_values, np.abs(np.array(approximations) - exact), 'bo-')
plt.axhline(y=0, color='red', linestyle='--', alpha=0.7)
plt.xlabel('Number of intervals (n)')
plt.ylabel('Absolute error')
plt.title('Convergence of Riemann Sum')
plt.grid(True)
plt.show()