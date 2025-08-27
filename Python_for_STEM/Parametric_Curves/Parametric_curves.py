import numpy as np
import matplotlib.pyplot as plt

# Parameter range
t = np.linspace(0, 2 * np.pi, 1000)

fig, axes = plt.subplots(2, 2, figsize=(12, 12))
fig.suptitle('Parametric Curves', fontsize=16)

# Circle
x_circle = np.cos(t)
y_circle = np.sin(t)
axes[0, 0].plot(x_circle, y_circle, '-b', linewidth=2)
axes[0, 0].set_title('Circle: $x=\\cos(t), y=\\sin(t)$')
axes[0, 0].set_aspect('equal')
axes[0, 0].grid(True)

# Ellipse
a, b = 3, 2
x_ellipse = a * np.cos(t)
y_ellipse = b * np.sin(t)
axes[0, 1].plot(x_ellipse, y_ellipse, 'r-', linewidth=2)
axes[0, 1].set_title(f'Ellipse: x={a}cos(t), y={b}sin(t)')
axes[0, 1].set_aspect('equal')
axes[0, 1].grid(True)

# Lissajous curve
x_liss = np.sin(3*t)
y_liss = np.sin(2*t)
axes[1, 0].plot(x_liss, y_liss, 'g-', linewidth=2)
axes[1, 0].set_title('Lissajous: x=sin(3t), y=sin(2t)')
axes[1, 0].set_aspect('equal')
axes[1, 0].grid(True)

# Cycloid
r = 1
x_cycloid = r * (t - np.sin(t))
y_cycloid = r * (1 - np.cos(t))
axes[1, 1].plot(x_cycloid, y_cycloid, 'm-', linewidth=2)
axes[1, 1].set_title('Cycloid: x=r(t-sin(t)), y=r(1-cos(t))')
axes[1, 1].grid(True)

plt.tight_layout()
plt.show()