import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Description: This program simulates a double pendulum and computes its Lyapunov exponent
# to quantify chaotic behavior.

# Parameters
g, L1, L2, m1, m2 = 9.81, 1.0, 1.0, 1.0, 1.0  # Gravity, Lengths, Masses
t = np.linspace(0, 10, 1000)

# Equations of motion
def pendulum(state, t):
    theta1, omega1, theta2, omega2 = state
    dtheta1 = omega1
    dtheta2 = omega2
    domega1 = (-g * (2 * m1 + m2) * np.sin(theta1) - m2 * g * np.sin(theta1 - 2 * theta2) -
               2 * np.sin(theta1 - theta2) * m2 * (L2 * omega2**2 + L1 * omega1**2 * np.cos(theta1 - theta2))) / \
              (L1 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2)))
    domega2 = (2 * np.sin(theta1 - theta2) * (L1 * omega1**2 * (m1 + m2) + g * (m1 + m2) * np.cos(theta1) +
               L2 * omega2**2 * m2 * np.cos(theta1 - theta2))) / \
              (L2 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2)))
    return [dtheta1, domega1, dtheta2, domega2]

# Initial conditions (perturbed for Lyapunov)
state0 = [np.pi / 2, 0, np.pi / 2, 0]
state0_pert = [np.pi / 2 + 1e-6, 0, np.pi / 2, 0]
sol = odeint(pendulum, state0, t)
sol_pert = odeint(pendulum, state0_pert, t)

# Lyapunov exponent (approximate)
dist = np.sqrt((sol[:, 0] - sol_pert[:, 0])**2 + (sol[:, 2] - sol_pert[:, 2])**2)
lyapunov = np.mean(np.log(dist[1:] / dist[:-1] + 1e-10)) / (t[1] - t[0])

# Plot
plt.figure(figsize=(10, 6))
plt.plot(sol[:, 0], sol[:, 1], label='Pendulum 1')
plt.plot(sol[:, 2], sol[:, 3], label='Pendulum 2')
plt.title(f'Double Pendulum (Lyapunov Exponent: {lyapunov:.4f})')
plt.xlabel('Angle (rad)')
plt.ylabel('Angular Velocity (rad/s)')
plt.legend()
plt.grid(True)
plt.show()