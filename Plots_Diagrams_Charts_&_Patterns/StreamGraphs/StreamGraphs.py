import matplotlib.pyplot as plt
import numpy as np 

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) + np.cos(x)

fig, ax = plt.subplots()
ax.fill_between(x, y1, color="skyblue", alpha=0.4)
ax.fill_between(x, y2, color="orange", alpha=0.4)
ax.fill_between(x, y3, color="green", alpha=0.4)
ax.set_title("Stream Graphs")

ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.legend(["sin(x)", "cos(x)", "sin(x) + cos(x)"], loc="upper right")
plt.gca().set_facecolor('lightgrey')
plt.grid(color='white', linestyle='--', linewidth=0.5)
plt.gca().set_axisbelow(True)
plt.show()

