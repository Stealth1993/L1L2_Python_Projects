import numpy as np
import matplotlib.pyplot as plt

# Description: This program simulates the exponential decay of a radioactive particle,
# such as a muon, using a Monte Carlo approach to model the number of remaining particles
# over time. It demonstrates particle physics concepts like half-life.

# Parameters
N0 = 10000  # Initial number of particles
tau = 2.2e-6  # Mean lifetime (s, e.g., muon)
t = np.linspace(0, 5e-6, 1000)  # Time (s)

# Decay probability
decay_prob = 1 - np.exp(-t / tau)
particles = N0 * np.exp(-t / tau)

# Monte Carlo simulation
rng = np.random.default_rng()
decays = rng.exponential(tau, N0)
decay_times = np.sort(decays)
remaining = N0 - np.arange(N0)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(t * 1e6, particles, 'b-', label='Analytical')
plt.step(decay_times * 1e6, remaining, 'r-', label='Monte Carlo', alpha=0.5)
plt.title('Particle Decay Simulation')
plt.xlabel('Time (μs)')
plt.ylabel('Number of Particles')
plt.legend()
plt.grid(True)
plt.show()