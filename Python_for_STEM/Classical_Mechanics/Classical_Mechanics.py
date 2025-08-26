import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class ClassicalMechanicsSimulator:
    def __init__(self):
        self.fig, self.axes = plt.subplots(2, 2, figsize=(14, 10))
        self.fig.suptitle('Classical Mechanics Simulations', fontsize=16)

    def pendulum_motion(self):
        """Single pendulum simulation"""
        g = 9.81
        L = 1.0
        theta0 = np.pi/4

        t = np.linspace(0, 10, 1000)
        omega = np.sqrt(g/L)
        theta = theta0 * np.cos(omega * t)

        x = L * np.sin(theta)
        y = L * np.cos(theta)

        self.axes[0, 0].plot(t, theta, '-b', linewidth=2)
        self.axes[0, 0].set_title('Pendulum Angle vs Time')
        self.axes[0, 0].set_xlabel('Time (s)')
        self.axes[0, 0].set_ylabel('Angle (rad)')
        self.axes[0, 0].grid(True)

    def projectile_motion(self):
        """Projectile motion with air resistance"""
        v0 = 50 # Initial velocity in m/s
        angles = [30, 45, 60] #Launch angles
        g = 9.81

        for angle in angles:
            theta = np.radians(angle)
            t_flight = 2 * v0 * np.sin(theta) / g
            t = np.linspace(0, t_flight, 100)

            x = v0 * np.cos(theta) * t
            y = v0 * np.sin(theta) * t - 0.5 * g * t**2

            self.axes[0, 1].plot(x, y, label=f'{angle}°', linewidth=2)

        self.axes[0, 1].set_title('Projectile Motion')
        self.axes[0, 1].set_xlabel('Distance (m)')
        self.axes[0, 1].set_ylabel('Height (m)')
        self.axes[0, 1].legend()
        self.axes[0, 1].grid(True)

    def harmonic_oscillator(self):
        """Damped harmonic oscillator"""
        t = np.linspace(0, 10, 1000)
        gamma_values = [0, 0.5, 1, 2] # Damping coefficients

        for gamma in gamma_values:
            if gamma == 0:
                y = np.cos(t)
                label = 'Undamped'
            elif gamma < 1:
                omega_d = np.sqrt(1 - gamma**2)
                y = np.exp(-gamma * t) * np.cos(omega_d * t)
                label = f'Underdamped (γ={gamma})'
            elif gamma == 1:
                y = (1 + t) * np.exp(-t)
                label = 'Critically Damped (γ=1)'
            else:
                y = 0.5 * np.exp(-t) * (np.exp(t*np.sqrt(gamma**2 - 1)) + np.exp(-t*np.sqrt(gamma**2 - 1)))
                label = f'Overdamped (γ={gamma})'

            self.axes[1, 0].plot(t , y, label=label, linewidth=2)

        self.axes[1, 0].set_title('Damped Harmonic Oscillator')
        self.axes[1, 0].set_xlabel('Time (s)')
        self.axes[1, 0].set_ylabel('Displacement (m)')
        self.axes[1, 0].legend()
        self.axes[1, 0].grid(True)

    def energy_conservation(self):
        """Energy conservation in pendulum"""
        g = 9.81
        L = 1.0
        theta0 = np.pi/3
        
        t = np.linspace(0, 4*np.pi/np.sqrt(g/L), 1000)
        theta = theta0 * np.cos(np.sqrt(g/L) * t)
        
        # Energies
        V = 0.5 * g * L * theta**2  # Potential energy (small angle approx)
        K = 0.5 * L**2 * (theta0 * np.sqrt(g/L))**2 * np.sin(np.sqrt(g/L) * t)**2
        E_total = V + K
        
        self.axes[1,1].plot(t, V, 'r-', label='Potential Energy', linewidth=2)
        self.axes[1,1].plot(t, K, 'b-', label='Kinetic Energy', linewidth=2)
        self.axes[1,1].plot(t, E_total, 'k--', label='Total Energy', linewidth=2)
        
        self.axes[1,1].set_title('Energy Conservation')
        self.axes[1,1].set_xlabel('Time (s)')
        self.axes[1,1].set_ylabel('Energy')
        self.axes[1,1].legend()
        self.axes[1,1].grid(True)
        
    def run_simulation(self):
        self.pendulum_motion()
        self.projectile_motion()
        self.harmonic_oscillator()
        self.energy_conservation()
        plt.tight_layout()
        plt.show()

# Usage
simulator = ClassicalMechanicsSimulator()
simulator.run_simulation()