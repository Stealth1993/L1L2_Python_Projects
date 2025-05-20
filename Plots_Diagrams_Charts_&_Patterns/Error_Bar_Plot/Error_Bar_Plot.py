import matplotlib.pyplot as plt
import numpy as np

# Sample data
x = np.linspace(0, 10, 10)
y = np.sin(x)
y_err = 0.1 + 0.1 * np.sqrt(x)
y_err2 = 0.1 + 0.1 * np.sqrt(x) / 2

# Create a figure and axis
fig, ax = plt.subplots()

# Plot with error bars
ax.errorbar(x, y, yerr=y_err, label='Error bars', fmt='o', color='blue', capsize=5)

# Plot with asymmetric error bars
ax.errorbar(x, y + 0.5, yerr=[y_err2, y_err], label='Asymmetric error bars', fmt='o', color='red', capsize=5)
ax.errorbar(x, y + 1, yerr=[y_err, y_err2], label='Asymmetric error bars (reversed)', fmt='o', color='green', capsize=5)    

# Add labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Error Bar Plot')
ax.legend()
ax.grid()
# Show the plot
plt.show()