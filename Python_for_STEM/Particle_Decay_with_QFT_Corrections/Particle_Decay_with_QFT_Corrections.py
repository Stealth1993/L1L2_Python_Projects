import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parameters
N0 = 1000  # Initial number of particles
tau1, tau2 = 2.2e-6, 1.0e-6  # Lifetimes of particles 1 and 2 in seconds
alpha = 1/137  # Fine-structure constant
branching_ratio = 0.7 # Branching ratio for particle 1 decay
t = np.linspace(0, 5e-6, 1000)  # Time array from 0 to 5 microseconds

# Decay rate with radiative corrections
def decay_rate(t, N, tau, alpha):
    return (N / tau) * (1 + alpha / np.pi)

# ODE system for particle decay
def model(N, t, tau1, tau2, alpha, branching_ratio):
    dN1_dt = -decay_rate(t, N[0], tau1, alpha) * branching_ratio
    dN2_dt = -decay_rate(t, N[1], tau2, alpha) * (1 - branching_ratio)
    return [dN1_dt, dN2_dt]

# Solve the ODE system
initial_conditions = [N0 * branching_ratio, N0 * (1 - branching_ratio)]
solution = odeint(model, initial_conditions, t, args=(tau1, tau2, alpha, branching_ratio))
# Extract results
N1 = solution[:, 0]
N2 = solution[:, 1]
# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(t * 1e6, N1, label='Particle 1', color
='blue')
plt.plot(t * 1e6, N2, label='Particle 2', color
='red')
plt.title('Particle Decay with QFT Corrections')
plt.xlabel('Time (microseconds)')
plt.ylabel('Number of Particles')
plt.legend()
plt.grid()
plt.show()
