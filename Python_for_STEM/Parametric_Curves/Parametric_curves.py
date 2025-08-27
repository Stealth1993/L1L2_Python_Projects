import numpy as np
import matplotlib.pyplot as plt

# Parameter range
t = np.linspace(0, 2 * np.pi, 1000)

fig, axes = plt.subplots(2, 2, figsize=(12, 12))
fig.suptitle('Parametric Curves', fontsize=16)

# Circle
x_circle = np.cos(t)
y_circle = np.sin(t)