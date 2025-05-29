# Description: This program performs Bayesian inference on a Gaussian signal using MCMC,
# estimating parameters with a Metropolis-Hastings algorithm.

# MCMC stands for Markov Chain Monte Carlo, a method used to sample from probability distributions.
# It is particularly useful in Bayesian inference for estimating posterior distributions.

# Required Libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


# Data
np.random.seed(42)
true_mean = 5
true_std = 1
data = np.random.normal(true_mean, true_std, size=100)  

# Prior parameters
prior_mean = 0
prior_std = 10

# Likelihood function
def likelihood(data, mean, std):
    return np.prod(norm.pdf(data, loc=mean, scale=std))

# Prior function
def prior(mean, std):
    return norm.pdf(mean, loc=prior_mean, scale=prior_std) * norm.pdf(std, loc=0, scale=1)

# Posterior function
def posterior(data, mean, std):
    return likelihood(data, mean, std) * prior(mean, std)

# Metropolis-Hastings algorithm
def metropolis_hastings(data, initial_mean, initial_std, iterations):
    samples = []
    current_mean = initial_mean
    current_std = initial_std

    for _ in range(iterations):
        proposed_mean = np.random.normal(current_mean, 0.5)
        proposed_std = np.abs(np.random.normal(current_std, 0.1))  # Ensure std is positive

        current_posterior = posterior(data, current_mean, current_std)
        proposed_posterior = posterior(data, proposed_mean, proposed_std)

        acceptance_ratio = proposed_posterior / current_posterior

        if np.random.rand() < acceptance_ratio:
            current_mean = proposed_mean
            current_std = proposed_std

        samples.append((current_mean, current_std))

    return np.array(samples)

# Run MCMC
initial_mean = 0
initial_std = 1
iterations = 1000
samples = metropolis_hastings(data, initial_mean, initial_std, iterations)

# Extract samples
means = samples[:, 0]
stds = samples[:, 1]
# Plot results
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.hist(means, bins=30, density=True, alpha=0.6, color='g', label='Sampled Means')
plt.axvline(true_mean, color='r', linestyle='dashed', linewidth=2, label='True Mean')
plt.title('Posterior Distribution of Mean')
plt.xlabel('Mean')
plt.ylabel('Density')
plt.legend()
plt.subplot(1, 2, 2)
plt.hist(stds, bins=30, density=True, alpha=0.6, color='b', label='Sampled Std Dev')
plt.axvline(true_std, color='r', linestyle='dashed', linewidth=2, label='True Std Dev')
plt.title('Posterior Distribution of Std Dev')
plt.xlabel('Standard Deviation')
plt.ylabel('Density')
plt.legend()
plt.tight_layout()
plt.show()

# Print estimated parameters
print(f"Estimated Mean: {np.mean(means):.2f}, Estimated Std Dev: {np.mean(stds):.2f}")

# Save the results
np.savez('bayesian_inference_results.npz', means=means, stds=stds, true_mean=true_mean, true_std=true_std)

# The code performs Bayesian inference using MCMC to estimate the mean and standard deviation of a Gaussian signal.
# The results are visualized with histograms and the estimated parameters are printed.
# The results are also saved to a .npz file for further analysis.
# The code is structured to be modular, with functions for likelihood, prior, posterior, and the MCMC algorithm.
# The use of numpy and matplotlib allows for efficient computation and visualization.
# The program is designed to be easily extensible for different prior distributions or likelihood functions.
# The code is well-commented to explain each step of the process.
# The program can be run in any Python environment with the required libraries installed.
# The code is efficient and should run quickly for the given data size.


# MCMC stands for Markov Chain Monte Carlo, a method used to sample from probability distributions.
# It is particularly useful in Bayesian inference for estimating posterior distributions.