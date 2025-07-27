import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Create figure
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('Probability Distributions', fontsize=16)

x = np.linspace(-5, 5, 1000)

# Normal distribution
for i, (mu, sigma) in enumerate([(0, 1), (0, 0.5), (1, 1)]):
    y = stats.norm.pdf(x, mu, sigma)
    axes[0, 0].plot(x, y, linewidth=2, label=f'μ={mu}, σ={sigma}')
axes[0, 0].set_title('Normal Distribution')
axes[0, 0].legend()
axes[0, 0].grid(True)

# Exponential distribution
x_exp = np.linspace(0, 5, 1000)
for i, lam in enumerate([0.5, 1, 2]):
    y = stats.expon.pdf(x_exp, scale=1/lam)
    axes[0, 1].plot(x_exp, y, linewidth=2, label=f'λ={lam}')
axes[0, 1].set_title('Exponential Distribution')
axes[0, 1].legend()
axes[0, 1].grid(True)

# Beta distribution
x_beta = np.linspace(0, 1, 1000)
for alpha, beta in [(2, 5), (5, 2), (2, 2)]:
    y = stats.beta.pdf(x_beta, alpha, beta)
    axes[0, 2].plot(x_beta, y, linewidth=2, label=f'α={alpha}, β={beta}')
axes[0, 2].set_title('Beta Distribution')
axes[0, 2].legend()
axes[0, 2].grid(True)

# Gamma distribution
x_gamma = np.linspace(0, 10, 1000)
for k, theta in [(1, 2), (2, 2), (3, 2)]:
    y = stats.gamma.pdf(x_gamma, k, scale=theta)
    axes[1, 0].plot(x_gamma, y, linewidth=2, label=f'k={k}, θ={theta}')
axes[1, 0].set_title('Gamma Distribution')
axes[1, 0].legend()
axes[1, 0].grid(True)

# Chi-square distribution
x_chi = np.linspace(0, 15, 1000)
for k in [1, 2, 3, 4]:
    y = stats.chi2.pdf(x_chi, k)
    axes[1, 1].plot(x_chi, y, linewidth=2, label=f'k={k}')
axes[1, 1].set_title('Chi-square Distribution')
axes[1, 1].legend()
axes[1, 1].grid(True)

# t-distribution
for df in [1, 2, 5, 30]:
    y = stats.t.pdf(x, df)
    axes[1, 2].plot(x, y, linewidth=2, label=f'df={df}')
# Add normal for comparison
axes[1, 2].plot(x, stats.norm.pdf(x), 'k--', linewidth=2, label='Normal')
axes[1, 2].set_title('t-Distribution')
axes[1, 2].legend()
axes[1, 2].grid(True)

plt.tight_layout()
plt.show()