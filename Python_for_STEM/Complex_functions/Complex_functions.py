import numpy as np
import matplotlib.pyplot as plt

def complex_function(z, func_type='polynomial'):
    """Various complex functions for demonstration."""
    if func_type == 'polynomial':
        return z**3 - 1
    elif func_type == 'exponential':
        return np.exp(z)
    elif func_type == 'sine':
        return np.sin(z)
    elif func_type == 'mobius':
        return (z - 1j) / (z + 1j)
    else:
        raise ValueError("Unknown function type. Choose from 'polynomial', 'exponential', 'sine', or 'mobius'.")
    
# Create complex plane
x = np.linspace(-3, 3, 30)
y = np.linspace(-3, 3, 30)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
fig.suptitle('Complex Function Visualizations', fontsize=16)

functions = ['polynomial', 'exponential', 'sine', 'mobius']
titles = ['f(z) = z³ - 1', 'f(z) = eᶻ', 'f(z) = sin(z)', 'f(z) = (z-i)/(z+i)']

for i, (func, title) in enumerate(zip(functions, titles)):
    W = complex_function(Z, func)
    
    # Magnitude plot
    axes[0, i].contourf(X, Y, np.abs(W), levels=20, cmap='viridis')
    axes[0, i].set_title(f'{title} - Magnitude')
    axes[0, i].set_aspect('equal')
    
    # Phase plot
    axes[1, i].contourf(X, Y, np.angle(W), levels=20, cmap='hsv')
    axes[1, i].set_title(f'{title} - Phase')
    axes[1, i].set_aspect('equal')

plt.tight_layout()
plt.show()