#This code simulates the motion of a double pendulum using numerical integration.
# It uses the Euler method to solve the equations of motion and plots the angles and angular velocities over time.
# Double Pendulum Chaos Simulation

import numpy as np
import matplotlib.pyplot as plt

# Parameters
g = 9.81  # acceleration due to gravity (m/s^2)
L1 = 1.0  # length of first pendulum (m)    
L2 = 1.0  # length of second pendulum (m)
m1 = 1.0  # mass of first pendulum (kg)
m2 = 1.0  # mass of second pendulum (kg)

# Initial conditions
theta1_0 = np.pi / 2  # initial angle of first pendulum (radians)
theta2_0 = np.pi / 2  # initial angle of second pendulum (radians)
theta1_dot_0 = 0.0  # initial angular velocity of first pendulum (rad/s)
theta2_dot_0 = 0.0  # initial angular velocity of second pendulum (rad/s)

# Time parameters
dt = 0.01  # time step (s)
t_max = 10.0  # total time (s)
t = np.arange(0, t_max, dt)  # time array
# Number of time steps
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
    
    # Update angular velocities
    theta1_dot[i + 1] = theta1_dot[i] + dtheta1_dot * dt
    theta2_dot[i + 1] = theta2_dot[i] + dtheta2_dot * dt
    
    # Update angles
    theta1[i + 1] = theta1[i] + theta1_dot[i] * dt
    theta2[i + 1] = theta2[i] + theta2_dot[i] * dt

# Plotting the results
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(t, theta1, label='Theta 1 (rad)')
plt.plot(t, theta2, label='Theta 2 (rad)')
plt.xlabel('Time (s)')
plt.ylabel('Angle (rad)')
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(t, theta1_dot, label='Theta 1 Dot (rad/s)')
plt.plot(t, theta2_dot, label='Theta 2 Dot (rad/s)')
plt.xlabel('Time (s)')
plt.ylabel('Angular Velocity (rad/s)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()