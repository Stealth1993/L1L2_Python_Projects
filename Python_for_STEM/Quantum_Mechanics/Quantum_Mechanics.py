import numpy as np
import matplotlib.pyplot as plt
from scipy.special import hermite
from scipy.integrate import solve_ivp

class QuantumMechanicsVisualizer:
    def __init__(self):
        self.hbar = 1.054571817e-34 # reduced Planck's constant
        self.m = 9.1093837015e-31  # electron mass
        
    def harmonic_oscillator_wavefunctions(self):
        """Quantum harmonic oscillator wavefunctions"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Quantum Harmonic Oscillator', fontsize=16)
        
        # Parameters
        omega = 1
        x = np.linspace(-4, 4, 1000)
        
        # Wavefunctions for n = 0, 1, 2, 3
        for n in range(4):
            # Normalization constant
            N_n = (omega/(np.pi))**(1/4) / np.sqrt(2**n * np.math.factorial(n))
            
            # Hermite polynomial
            H_n = hermite(n)
            xi = np.sqrt(omega) * x
            
            # Wavefunction
            psi_n = N_n * np.exp(-xi**2/2) * H_n(xi)
            
            # Probability density
            prob_density = np.abs(psi_n)**2
            
            # Energy levels
            E_n = (n + 0.5) * omega
            
            row, col = divmod(n, 2)
            
            # Plot wavefunction
            axes[row, col].plot(x, psi_n, 'b-', linewidth=2, label=f'ψ_{n}(x)')
            axes[row, col].plot(x, prob_density, 'r--', linewidth=2, label=f'|ψ_{n}|²')
            axes[row, col].axhline(y=E_n, color='g', linestyle=':', alpha=0.7, label=f'E_{n} = {E_n:.1f}')
            
            # Classical turning points
            x_turn = np.sqrt(2*E_n/omega)
            axes[row, col].axvline(x=x_turn, color='orange', linestyle='--', alpha=0.5)
            axes[row, col].axvline(x=-x_turn, color='orange', linestyle='--', alpha=0.5)
            
            axes[row, col].set_title(f'n = {n}, E = {E_n:.1f}ℏω')
            axes[row, col].legend()
            axes[row, col].grid(True)
            axes[row, col].set_xlabel('Position (x)')
            axes[row, col].set_ylabel('Amplitude')
        
        plt.tight_layout()
        plt.show()
        
    def wave_packet_evolution(self):
        """Time evolution of a Gaussian wave packet"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Wave Packet Evolution', fontsize=16)
        
        # Parameters
        x = np.linspace(-10, 10, 500)
        k0 = 2  # initial momentum
        x0 = -3  # initial position
        sigma = 1  # width
        
        times = [0, 0.5, 1.0, 2.0]
        
        for i, t in enumerate(times):
            # Gaussian wave packet (free particle)
            sigma_t = sigma * np.sqrt(1 + (t/(2*sigma**2))**2)
            x_t = x0 + k0 * t / sigma**2
            
            # Wavefunction
            psi = (1/(sigma_t * np.sqrt(2*np.pi)))**(1/2) * \
                  np.exp(1j * k0 * (x - x_t)) * \
                  np.exp(-(x - x_t)**2 / (4 * sigma_t**2))
            
            prob_density = np.abs(psi)**2
            real_part = np.real(psi)
            imag_part = np.imag(psi)
            
            row, col = divmod(i, 2)
            
            axes[row, col].plot(x, prob_density, 'r-', linewidth=3, label='|ψ(x,t)|²')
            axes[row, col].plot(x, real_part, 'b--', alpha=0.7, label='Re[ψ(x,t)]')
            axes[row, col].plot(x, imag_part, 'g--', alpha=0.7, label='Im[ψ(x,t)]')
            
            axes[row, col].set_title(f'Time t = {t:.1f}')
            axes[row, col].legend()
            axes[row, col].grid(True)
            axes[row, col].set_xlabel('Position (x)')
            axes[row, col].set_ylabel('Amplitude')
        
        plt.tight_layout()
        plt.show()
        
    def quantum_tunneling(self):
        """Quantum tunneling through a barrier"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Quantum Tunneling', fontsize=16)
        
        # Parameters
        x = np.linspace(-5, 5, 1000)
        V0 = 2  # barrier height
        a = 1   # barrier width
        E = 1   # particle energy (< V0)
        
        # Potential
        V = np.zeros_like(x)
        V[np.abs(x) < a] = V0
        
        # Wave numbers
        k1 = np.sqrt(2 * E)  # outside barrier
        k2 = np.sqrt(2 * (V0 - E))  # inside barrier (imaginary)
        
        # Transmission coefficient (simplified)
        T = 1 / (1 + (V0**2 * np.sinh(k2 * 2*a)**2) / (4*E*(V0-E)))
        
        ax1.plot(x, V, 'k-', linewidth=3, label='Potential V(x)')
        ax1.axhline(y=E, color='r', linestyle='--', linewidth=2, label=f'Energy E = {E}')
        ax1.fill_between(x, 0, V, alpha=0.3, color='gray')
        ax1.set_title(f'Potential Barrier (Transmission = {T:.3f})')
        ax1.set_xlabel('Position (x)')
        ax1.set_ylabel('Energy')
        ax1.legend()
        ax1.grid(True)
        
        # Wavefunction (schematic)
        psi = np.zeros_like(x, dtype=complex)
        
        # Region 1: x < -a
        mask1 = x < -a
        psi[mask1] = np.sin(k1 * x[mask1]) + 0.5 * np.sin(k1 * x[mask1] + np.pi)
        
        # Region 2: |x| < a (inside barrier)
        mask2 = np.abs(x) < a
        psi[mask2] = 0.5 * np.exp(-k2 * np.abs(x[mask2]))
        
        # Region 3: x > a
        mask3 = x > a
        psi[mask3] = np.sqrt(T) * np.sin(k1 * x[mask3])
        
        ax2.plot(x, np.real(psi), 'b-', linewidth=2, label='Re[ψ(x)]')
        ax2.plot(x, np.abs(psi)**2, 'r-', linewidth=2, label='|ψ(x)|²')
        ax2.plot(x, V/5, 'k--', alpha=0.5, label='V(x)/5')
        ax2.set_title('Tunneling Wavefunction')
        ax2.set_xlabel('Position (x)')
        ax2.set_ylabel('Amplitude')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show()
        
    def run_all_visualizations(self):
        self.harmonic_oscillator_wavefunctions()
        self.wave_packet_evolution()
        self.quantum_tunneling()

# Usage
quantum_viz = QuantumMechanicsVisualizer()
quantum_viz.run_all_visualizations()