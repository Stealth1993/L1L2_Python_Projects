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
        