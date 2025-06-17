import numpy as np
import matplotlib.pyplot as plt

# Parameters for the simulation
num_particles = 1000  # Total number of particles
decay_probability = 0.1  # Probability of decay per time step
time_steps = 50  # Number of time steps to simulate

# Initialize particle states
particles = np.ones(num_particles)

# Store the number of surviving particles at each time step
survivors = []

# Run the simulation
for t in range(time_steps):
    # Simulate decay
    decay = np.random.rand(num_particles) < decay_probability
    particles[decay] = 0  # Mark decayed particles
    survivors.append(np.sum(particles))

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(survivors, label='Surviving Particles', color='blue')
plt.xlabel('Time Step')
plt.ylabel('Number of Surviving Particles')
plt.title('Particle Decay Simulation')
plt.legend()
plt.grid(True)
plt.show()