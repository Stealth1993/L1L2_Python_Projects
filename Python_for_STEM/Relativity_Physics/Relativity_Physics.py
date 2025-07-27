import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class RelativityVisualizer:
    def __init__(self):
        self.c = 299792458  # Speed of light
        
    def lorentz_transformations(self):
        """Visualize Lorentz transformations and spacetime diagrams"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Special Relativity Effects', fontsize=16)
        
        # Velocity range
        v = np.linspace(0, 0.99*self.c, 1000)
        beta = v / self.c
        gamma = 1 / np.sqrt(1 - beta**2)
        
        # Lorentz factor
        axes[0,0].plot(beta, gamma, 'b-', linewidth=3)
        axes[0,0].set_xlabel('β = v/c')
        axes[0,0].set_ylabel('γ (Lorentz factor)')
        axes[0,0].set_title('Lorentz Factor vs Velocity')
        axes[0,0].grid(True)
        axes[0,0].set_ylim(1, 10)
        
        # Time dilation and length contraction
        proper_time = 1  # proper time/length
        dilated_time = gamma * proper_time
        contracted_length = proper_time / gamma
        
        axes[0,1].plot(beta, dilated_time, 'r-', linewidth=3, label='Time dilation')
        axes[0,1].plot(beta, contracted_length, 'g-', linewidth=3, label='Length contraction')
        axes[0,1].set_xlabel('β = v/c')
        axes[0,1].set_ylabel('Factor')
        axes[0,1].set_title('Time Dilation & Length Contraction')
        axes[0,1].legend()
        axes[0,1].grid(True)
        axes[0,1].set_ylim(0, 5)
        
        # Spacetime diagram
        t = np.linspace(-5, 5, 100)
        x = np.linspace(-5, 5, 100)
        
        # Light cone
        axes[1,0].plot(t, t, 'y-', linewidth=3, label='Light ray (c)')
        axes[1,0].plot(t, -t, 'y-', linewidth=3)
        
        # World lines for different velocities
        velocities = [0, 0.3*self.c, 0.6*self.c, 0.9*self.c]
        colors = ['k', 'b', 'g', 'r']
        
        for i, vel in enumerate(velocities):
            beta_v = vel / self.c if vel > 0 else 0
            world_line = beta_v * t if vel > 0 else np.zeros_like(t)
            label = f'v = {beta_v:.1f}c' if vel > 0 else 'Rest frame'
            axes[1,0].plot(world_line, t, colors[i], linewidth=2, label=label)
        
        axes[1,0].set_xlabel('Space (x)')
        axes[1,0].set_ylabel('Time (ct)')
        axes[1,0].set_title('Spacetime Diagram')
        axes[1,0].legend()
        axes[1,0].grid(True)
        axes[1,0].set_xlim(-3, 3)
        axes[1,0].set_ylim(-3, 3)
        
        # Relativistic energy-momentum
        m0 = 1  # rest mass (arbitrary units)
        p = np.linspace(0, 5*m0*self.c, 1000)  # momentum
        
        # Total energy
        E_total = np.sqrt((p*self.c)**2 + (m0*self.c**2)**2)
        
        # Classical kinetic energy
        E_classical = p**2 / (2*m0) + m0*self.c**2
        
        # Relativistic kinetic energy
        E_kinetic_rel = E_total - m0*self.c**2
        
        axes[1,1].plot(p/(m0*self.c), E_total/(m0*self.c**2), 'b-', 
                      linewidth=3, label='Total energy')
        axes[1,1].plot(p/(m0*self.c), E_kinetic_rel/(m0*self.c**2), 'r-', 
                      linewidth=3, label='Relativistic KE')
        axes[1,1].plot(p/(m0*self.c), (E_classical-m0*self.c**2)/(m0*self.c**2), 'g--', 
                      linewidth=2, label='Classical KE')
        
        axes[1,1].set_xlabel('p/(mc)')
        axes[1,1].set_ylabel('E/(mc²)')
        axes[1,1].set_title('Energy-Momentum Relation')
        axes[1,1].legend()
        axes[1,1].grid(True)
        axes[1,1].set_xlim(0, 5)
        
        plt.tight_layout()
        plt.show()
        
    def general_relativity_effects(self):
        """Visualize general relativity effects"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('General Relativity Effects', fontsize=16)
        
        # Gravitational time dilation
        r = np.linspace(1.1, 10, 1000)  # Distance from center (in Schwarzschild radii)
        Rs = 1  # Schwarzschild radius (units)
        
        # Time dilation factor
        time_dilation = np.sqrt(1 - Rs/r)
        
        axes[0,0].plot(r, time_dilation, 'b-', linewidth=3)
        axes[0,0].axvline(x=Rs, color='r', linestyle='--', 
                         label='Event horizon (r = Rs)')
        axes[0,0].set_xlabel('r/Rs')
        axes[0,0].set_ylabel('√(1 - Rs/r)')
        axes[0,0].set_title('Gravitational Time Dilation')
        axes[0,0].legend()
        axes[0,0].grid(True)
        axes[0,0].set_xlim(1, 10)
        
        # Gravitational redshift
        redshift_factor = 1/time_dilation - 1
        
        axes[0,1].plot(r, redshift_factor, 'r-', linewidth=3)
        axes[0,1].set_xlabel('r/Rs')
        axes[0,1].set_ylabel('Redshift z')
        axes[0,1].set_title('Gravitational Redshift')
        axes[0,1].grid(True)
        axes[0,1].set_xlim(1, 10)
        axes[0,1].set_ylim(0, 5)
        
        # Precession of Mercury (simplified)
        theta = np.linspace(0, 8*np.pi, 1000)
        
        # Classical ellipse
        e = 0.2  # eccentricity
        a = 1    # semi-major axis
        r_classical = a * (1 - e**2) / (1 + e * np.cos(theta))
        
        # With relativistic correction (exaggerated)
        delta_phi = 0.1  # precession per orbit (exaggerated)
        r_relativistic = a * (1 - e**2) / (1 + e * np.cos(theta - delta_phi * theta/(2*np.pi)))
        
        x_classical = r_classical * np.cos(theta)
        y_classical = r_classical * np.sin(theta)
        x_relativistic = r_relativistic * np.cos(theta)
        y_relativistic = r_relativistic * np.sin(theta)
        
        axes[1,0].plot(x_classical, y_classical, 'b-', linewidth=2, 
                      label='Classical orbit')
        axes[1,0].plot(x_relativistic, y_relativistic, 'r-', linewidth=2, 
                      label='Relativistic orbit')
        axes[1,0].plot(0, 0, 'yo', markersize=8, label='Sun')
        axes[1,0].set_xlabel('x')
        axes[1,0].set_ylabel('y')
        axes[1,0].set_title('Orbital Precession')
        axes[1,0].legend()
        axes[1,0].set_aspect('equal')
        axes[1,0].grid(True)
        
        # Light bending near massive object
        # Impact parameter range
        b = np.linspace(1.5, 5, 100)  # Impact parameter
        Rs = 1  # Schwarzschild radius
        
        # Deflection angle (small angle approximation)
        deflection_angle = 2 * Rs / b  # in radians
        
        axes[1,1].plot(b, np.degrees(deflection_angle), 'g-', linewidth=3)
        axes[1,1].set_xlabel('Impact parameter b/Rs')
        axes[1,1].set_ylabel('Deflection angle (degrees)')
        axes[1,1].set_title('Light Deflection')
        axes[1,1].grid(True)
        axes[1,1].set_yscale('log')
        
        plt.tight_layout()
        plt.show()
        
    def run_all_visualizations(self):
        self.lorentz_transformations()
        self.general_relativity_effects()

# Usage
relativity_viz = RelativityVisualizer()
relativity_viz.run_all_visualizations()