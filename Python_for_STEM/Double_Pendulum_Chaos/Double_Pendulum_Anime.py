import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# Parameters
g = 9.81  # acceleration due to gravity (m/s^2)
L1 = 1.0  # length of first pendulum (m)    
L2 = 1.0  # length of second pendulum (m)
m1 = 1.0  # mass of first pendulum (kg)
m2 = 1.0  # mass of second pendulum (kg)

# Initial conditions
theta1_0 = np.pi / 2  # initial angle of first pendulum (radians)
theta2_0 = np.pi / 2  # initial angle of second pendulum (radians)
theta1_dot_0 = 0.0    # initial angular velocity of first pendulum (rad/s)
theta2_dot_0 = 0.0    # initial angular velocity of second pendulum (rad/s)

# Time parameters
dt = 0.01  # time step (s)
t_max = 10.0  # total time (s)
t = np.arange(0, t_max, dt)  # time array
n_steps = len(t)

# Initialize arrays to store angles and angular velocities
theta1 = np.zeros(n_steps)
theta2 = np.zeros(n_steps)
theta1_dot = np.zeros(n_steps)
theta2_dot = np.zeros(n_steps)

# Set initial conditions
theta1[0] = theta1_0
theta2[0] = theta2_0
theta1_dot[0] = theta1_dot_0
theta2_dot[0] = theta2_dot_0

# Function to compute derivatives
def derivatives(theta1, theta2, theta1_dot, theta2_dot):
    delta = theta2 - theta1
    den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta) ** 2
    den2 = (L2 / L1) * den1

    dtheta1_dot = (m2 * L1 * theta1_dot ** 2 * np.sin(delta) * np.cos(delta) +
                   m2 * g * np.sin(theta2) * np.cos(delta) +
                   m2 * L2 * theta2_dot ** 2 * np.sin(delta) -
                   (m1 + m2) * g * np.sin(theta1)) / den1

    dtheta2_dot = (-m2 * L2 * theta2_dot ** 2 * np.sin(delta) * np.cos(delta) +
                   (m1 + m2) * g * np.sin(theta1) * np.cos(delta) -
                   (m1 + m2) * L1 * theta1_dot ** 2 * np.sin(delta)) / den2

    return dtheta1_dot, dtheta2_dot

# Time integration using Euler's method
for i in range(n_steps - 1):
    dtheta1_dot, dtheta2_dot = derivatives(theta1[i], theta2[i], theta1_dot[i], theta2_dot[i])
    theta1_dot[i + 1] = theta1_dot[i] + dtheta1_dot * dt
    theta2_dot[i + 1] = theta2_dot[i] + dtheta2_dot * dt
    theta1[i + 1] = theta1[i] + theta1_dot[i] * dt
    theta2[i + 1] = theta2[i] + theta2_dot[i] * dt

# Compute positions for animation
x1 = L1 * np.sin(theta1)
y1 = -L1 * np.cos(theta1)
x2 = x1 + L2 * np.sin(theta2)
y2 = y1 - L2 * np.cos(theta2)

# Set up the plot for animation
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)
ax.set_aspect('equal')
ax.set_title('Double Pendulum Animation')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')

# Initialize the line object for the pendulum
line, = ax.plot([], [], 'o-', lw=2, markersize=10)

# Animation function
def animate(i):
    line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
    return line,

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=n_steps, interval=20, blit=True)

# Display the animation
plt.show()