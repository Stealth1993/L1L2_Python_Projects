import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parameters
g, L1, L2, m1, m2 = 9.81, 1.0, 1.0, 1.0, 1.0
t = np.linspace(0, 10, 1000)  # time array

# Equations of motion for the double pendulum
def equations_of_motion(state, t, g, L1, L2, m1, m2):
    theta1, omega1, theta2, omega2 = state
    delta = theta1 - theta2
    den = m1 + m2 * np.sin(delta)**2
    
    domega1 = (m2 * L2 * omega2**2 * np.sin(delta) - m2 * g * np.sin(theta2) * np.cos(delta)
               - (m1 + m2) * g * np.sin(theta1)) / (L1 * den)
    domega2 = ((m1 + m2) * (L1 * omega1**2 * np.sin(delta) + g * np.sin(theta1) * np.cos(delta))
               + m2 * g * np.sin(theta2)) / (L2 * den)
    
    return [omega1, domega1, omega2, domega2]

# Initial conditions
def initial_conditions():
    theta1_0 = np.pi / 2  # initial angle of first pendulum (radians)
    omega1_0 = 0.0        # initial angular velocity of first pendulum (rad/s)
    theta2_0 = np.pi / 2  # initial angle of second pendulum (radians)
    omega2_0 = 0.0        # initial angular velocity of second pendulum (rad/s)
    return [theta1_0, omega1_0, theta2_0, omega2_0]

# Integrate the equations of motion
def integrate_double_pendulum():
    y0 = initial_conditions()
    sol = odeint(equations_of_motion, y0, t, args=(g, L1, L2, m1, m2))
    return sol

# Main function to run the simulation and plot results
def main():
    sol = integrate_double_pendulum()

    # Plotting the results
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(t, sol[:, 0], label='Theta 1 (rad)')
    plt.plot(t, sol[:, 2], label='Theta 2 (rad)')
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (rad)')
    plt.legend()
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(t, sol[:, 1], label='Omega 1 (rad/s)')
    plt.plot(t, sol[:, 3], label='Omega 2 (rad/s)')
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Velocity (rad/s)')
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()