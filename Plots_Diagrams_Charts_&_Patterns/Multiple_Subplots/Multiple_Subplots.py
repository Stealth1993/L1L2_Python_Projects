import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

fig, ax = plt.subplots(2, 2, figsize=(10, 6))
fig.suptitle('Multiple Subplots Example')

ax[0, 0].plot(x, np.sin(x), 'r-')
ax[0, 0].set_title('Sine Function')
ax[0, 0].set_xlabel('x')
ax[0, 0].set_ylabel('sin(x)')

ax[0, 1].plot(x, np.cos(x), 'g-')
ax[0, 1].set_title('Cosine Function')
ax[0, 1].set_xlabel('x')
ax[0, 1].set_ylabel('cos(x)')

ax[1, 0].plot(x, np.tan(x), 'b-')
ax[1, 0].set_title('Tangent Function')
ax[1, 0].set_xlabel('x')
ax[1, 0].set_ylabel('tan(x)')

ax[1, 0].set_ylim(-10, 10)  # Limit y-axis for tangent function

ax[1, 1].plot(x, np.exp(x), 'm-')
ax[1, 1].set_title('Exponential Function')
ax[1, 1].set_xlabel('x')
ax[1, 1].set_ylabel('exp(x)')

ax[1, 1].set_yscale('log')  # Log scale for exponential function
ax[1, 1].set_ylim(1, 10000)  # Limit y-axis for exponential function

plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout to make room for the title
plt.show()