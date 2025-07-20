# Visualize derivatives in Python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the function (example: f(x) = x^3)
def expr(x):
    return x**3

# Define the derivative of the function (f'(x) = 3x^2)
def expr_der(x):
    return 3*x**2

# Create values for function
values = np.linspace(-10, 10, 100)

# Plot the original function
plt.figure(figsize=(10, 6))
plt.plot(values, expr(values), label='f(x) = x³', linewidth=2)

# Define point of tangency
x1 = -5
y1 = expr(x1)

# Create range for tangent line
xrange = np.linspace(x1 - 5, x1 + 5, 10)

# Define tangent line function
def line(x, x1, y1):
    return expr_der(x1) * (x - x1) + y1

# Plot the tangent line
plt.plot(xrange, line(xrange, x1, y1), '--', 
         label=f'Tangent line at x = {x1}', linewidth=2)

# Mark the point of tangency
plt.scatter(x1, y1, s=100, c='red', zorder=5, 
           label=f'Point ({x1}, {y1})')

# Add labels and formatting
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.title('Function and Its Tangent Line', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='black', linewidth=0.5)
plt.axvline(x=0, color='black', linewidth=0.5)

# Show the plot
plt.show()

# Print derivative information
print(f"Function: f(x) = x³")
print(f"Derivative: f'(x) = 3x²")
print(f"At x = {x1}:")
print(f"  Function value: f({x1}) = {y1}")
print(f"  Derivative value: f'({x1}) = {expr_der(x1)}")
print(f"  Slope of tangent line: {expr_der(x1)}")
