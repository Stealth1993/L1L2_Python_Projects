import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

# Parameters
g , L1, L2, m1, m2 = 9.81, 1.0, 1.0, 1.0, 1.0

t = np.linspace(0, 10, 1000)  # time array

# Equations of motion for the double pendulum
def equations_of_motion(y, t, g, L1, L2, m1, m2):
    theta1, theta2, p1, p2 = y
    dtheta1_dt = p1 / (m1 * L1**2)
    dtheta2_dt = p2 / (m2 * L2**2)
    
    delta = theta2 - theta1
    d_p1_dt = -m2 * L1 * dtheta1_dt**2 * np.sin(delta) - (m1 + m2) * g * np.sin(theta1)
    d_p2_dt = m2 * L2 * dtheta2_dt**2 * np.sin(delta) + (m1 + m2) * g * np.sin(theta1) * np.cos(delta)
    
    return [dtheta1_dt, dtheta2_dt, d_p1_dt, d_p2_dt]

# Initial conditions
def initial_conditions():
    theta1_0 = np.pi / 2  # initial angle of first pendulum (radians)
    theta2_0 = np.pi / 2  # initial angle of second pendulum (radians)
    p1_0 = 0.0  # initial momentum of first pendulum
    p2_0 = 0.0  # initial momentum of second pendulum
    return [theta1_0, theta2_0, p1_0, p2_0]

# Integrate the equations of motion
def integrate_double_pendulum():
    y0 = initial_conditions()
    sol = integrate.odeint(equations_of_motion, y0, t, args=(g, L1, L2, m1, m2))
    return sol

# Calculate Lyapunov exponents
def lyapunov_exponents(sol):
    # Compute the Jacobian matrix and its eigenvalues
    # For simplicity, we'll use a placeholder implementation
    # In practice, you would compute the actual Jacobian
    J = np.eye(4)  # Placeholder for the Jacobian
    eigenvalues = np.linalg.eigvals(J)
    return np.log(np.abs(eigenvalues))

# Main function to run the simulation and plot results
def main():
    sol = integrate_double_pendulum()
    lyapunov_exp = lyapunov_exponents(sol)

    # Plotting the results
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(t, sol[:, 0], label='Theta 1 (rad)')
    plt.plot(t, sol[:, 1], label='Theta 2 (rad)')
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (rad)')
    plt.legend()
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(t, lyapunov_exp, label='Lyapunov Exponents')
    plt.xlabel('Time (s)')
    plt.ylabel('Lyapunov Exponent')
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()

