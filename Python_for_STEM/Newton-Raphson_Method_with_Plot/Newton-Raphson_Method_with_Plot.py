import numpy as np
import matplotlib.pyplot as plt

# Define the function and its derivative
def f(x):
    return x**2 - 2
def df(x):
    return 2*x
# Newton-Raphson method implementation
def newton_raphson(x0, tol=1e-6, max_iter=100):
    x = x0
    iterations = [x]  # Store iterations for plotting
    for i in range(max_iter):
        x_new = x - f(x) / df(x)  # Newton-Raphson formula
        iterations.append(x_new)
        if abs(x_new - x) < tol:  # Check convergence
            return x_new, iterations
        x = x_new
    raise ValueError("Method did not converge within max iterations")

# Test data
initial_guess = 1.5
print(f"Starting with initial guess: {initial_guess}")
# Run Newton-Raphson
root, iterations = newton_raphson(initial_guess)
# Output result
print(f"Approximate root: {root}")
print(f"Number of iterations: {len(iterations) - 1}")
# Generate data for plotting
x_values = np.linspace(0, 2, 100)
y_values = f(x_values)
# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x_values, y_values, label='f(x) = x² - 2', color='blue')
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
# Plot iteration points
for i, x_iter in enumerate(iterations):
    plt.scatter(x_iter, f(x_iter), color='red', zorder=5)
    plt.text(x_iter, f(x_iter), f'Iter {i}', ha='right', va='bottom')

plt.title('Newton-Raphson Method Convergence')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)
plt.show()

# This code implements the Newton-Raphson method to find the root of the function f(x) = x² - 2.
# It also plots the function and the iterations of the method to visualize convergence.
# This code implements the Newton-Raphson method to find the root of the function f(x) = x² - 2.
# It also plots the function and the iterations of the method to visualize convergence.
# The function f(x) = x² - 2 has a root at x = sqrt(2), which is approximately 1.414.
# The function f(x) = x² - 2 has a root at x = sqrt(2), which is approximately 1.414.
# The Newton-Raphson method is an iterative method that uses the derivative of the function to find the root.

# Application of the Newton-Raphson method is common in numerical analysis and optimization problems.