import numpy as np
import matplotlib.pyplot as plt

# Bell State Parameters
bell_state = np.array([[1, 0], [0, 1]]) / np.sqrt(2)  # Bell state |Φ+⟩ = (|00⟩ + |11⟩) / √2

# Measurement angles
theta = np.linspace(0, 2 * np.pi, 100)

# Calculate probabilities for each angle
prob_00 = np.zeros_like(theta)
prob_11 = np.zeros_like(theta)

for i, angle in enumerate(theta):
    # Measurement in the Bell basis
    measurement_vector = np.array([np.cos(angle), np.sin(angle)])
    
    # Probability of measuring |00⟩
    prob_00[i] = np.abs(np.dot(bell_state[0], measurement_vector))**2
    
    # Probability of measuring |11⟩
    prob_11[i] = np.abs(np.dot(bell_state[1], measurement_vector))**2

# Plotting the probabilities
plt.figure(figsize=(10, 6))
plt.plot(theta, prob_00, label='Probability of |00⟩', color='blue')
plt.plot(theta, prob_11, label='Probability of |11⟩', color='red')
plt.title('Bell State Measurement Probabilities')
plt.xlabel('Measurement Angle (θ)')
plt.ylabel('Probability')
plt.legend()
plt.grid()
plt.show()
# This code visualizes the measurement probabilities of a Bell state in the Bell basis.
# It calculates the probabilities of measuring the states |00⟩ and |11⟩ as a function of the measurement angle θ.
# The Bell state is defined as |Φ+⟩ = (|00⟩ + |11⟩) / √2, and the probabilities are computed using the inner product with the measurement vector.