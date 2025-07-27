import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ParticlePhysicsSimulator:
    def __init__(self):
        self.c = 1  # Speed of light (natural units)
        
    def particle_decay_visualization(self):
        """Visualize particle decay processes"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Particle Physics Processes', fontsize=16)
        
        # Exponential decay
        t = np.linspace(0, 5, 1000)
        tau_values = [0.5, 1.0, 1.5, 2.0]  # Different lifetimes
        
        for tau in tau_values:
            N = np.exp(-t/tau)
            axes[0,0].plot(t, N, linewidth=3, label=f'τ = {tau}')
        
        axes[0,0].set_xlabel('Time (units of τ)')
        axes[0,0].set_ylabel('N(t)/N₀')
        axes[0,0].set_title('Exponential Decay')
        axes[0,0].legend()
        axes[0,0].grid(True)
        axes[0,0].set_yscale('log')
        
        # Invariant mass distribution
        # Simulate Z boson decay to muon pairs
        np.random.seed(42)
        n_events = 10000
        
        # Z boson mass and width
        M_Z = 91.2  # GeV
        Gamma_Z = 2.5  # GeV
        
        # Generate invariant masses (Breit-Wigner distribution)
        masses = np.random.normal(M_Z, Gamma_Z/2, n_events)
        masses = masses[masses > 0]  # Physical masses only
        
        axes[0,1].hist(masses, bins=50, alpha=0.7, density=True, 
                      color='blue', edgecolor='black')
        
        # Theoretical Breit-Wigner
        m_range = np.linspace(80, 100, 1000)
        breit_wigner = (Gamma_Z/2)**2 / ((m_range - M_Z)**2 + (Gamma_Z/2)**2)
        breit_wigner /= np.max(breit_wigner) * np.max(axes[0,1].get_ylim())
        
        axes[0,1].plot(m_range, breit_wigner, 'r-', linewidth=3, 
                      label='Breit-Wigner')
        axes[0,1].axvline(x=M_Z, color='green', linestyle='--', 
                         label=f'M_Z = {M_Z} GeV')
        axes[0,1].set_xlabel('Invariant Mass (GeV)')
        axes[0,1].set_ylabel('Events')
        axes[0,1].set_title('Z Boson Peak')
        axes[0,1].legend()
        axes[0,1].grid(True)
        
        # Feynman diagram representation (artistic)
        # Two-particle collision producing new particles
        x_positions = [0, 2, 4, 6]
        y_positions = [0, 0, 1, -1]
        
        # Incoming particles
        axes[1,0].arrow(-2, 0.5, 2, -0.5, head_width=0.1, head_length=0.1, 
                       fc='blue', ec='blue', linewidth=2)
        axes[1,0].arrow(-2, -0.5, 2, 0.5, head_width=0.1, head_length=0.1, 
                       fc='blue', ec='blue', linewidth=2)
        
        # Vertex
        axes[1,0].plot(0, 0, 'ro', markersize=8)
        
        # Outgoing particles
        axes[1,0].arrow(0, 0, 2, 0.8, head_width=0.1, head_length=0.1, 
                       fc='red', ec='red', linewidth=2)
        axes[1,0].arrow(0, 0, 2, -0.8, head_width=0.1, head_length=0.1, 
                       fc='red', ec='red', linewidth=2)
        
        axes[1,0].text(-2, 0.7, 'e⁻', fontsize=14, ha='center')
        axes[1,0].text(-2, -0.7, 'e⁺', fontsize=14, ha='center')
        axes[1,0].text(2.5, 0.8, 'μ⁻', fontsize=14, ha='center')
        axes[1,0].text(2.5, -0.8, 'μ⁺', fontsize=14, ha='center')
        
        axes[1,0].set_xlim(-3, 3)
        axes[1,0].set_ylim(-2, 2)
        axes[1,0].set_title('e⁺e⁻ → μ⁺μ⁻ Process')
        axes[1,0].set_aspect('equal')
        axes[1,0].axis('off')
        
        # Cross-section vs energy
        # Simplified resonance behavior
        E_cm = np.linspace(80, 100, 1000)  # Center of mass energy
        
        # Background + resonance
        sigma_bg = 1.0  # Background cross-section
        sigma_resonance = 100 * breit_wigner / np.max(breit_wigner)
        
        total_cross_section = sigma_bg + sigma_resonance
        
        axes[1,1].plot(E_cm, total_cross_section, 'purple', linewidth=3)
        axes[1,1].axvline(x=M_Z, color='green', linestyle='--', 
                         label=f'M_Z = {M_Z} GeV')
        axes[1,1].set_xlabel('Center of Mass Energy (GeV)')
        axes[1,1].set_ylabel('Cross Section (arbitrary units)')
        axes[1,1].set_title('e⁺e⁻ → μ⁺μ⁻ Cross Section')
        axes[1,1].legend()
        axes[1,1].grid(True)
        
        plt.tight_layout()
        plt.show()
        
    def standard_model_visualization(self):
        """Visualize Standard Model particles and interactions"""
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        fig.suptitle('Standard Model of Particle Physics', fontsize=16)
        
        # Particle mass spectrum
        particles = {
            'Quarks': {'up': 0.002, 'down': 0.005, 'charm': 1.3, 'strange': 0.1, 
                      'top': 173, 'bottom': 4.2},
            'Leptons': {'electron': 0.000511, 'muon': 0.106, 'tau': 1.777,
                       'nu_e': 0, 'nu_mu': 0, 'nu_tau': 0},
            'Bosons': {'photon': 0, 'W': 80.4, 'Z': 91.2, 'Higgs': 125, 'gluon': 0}
        }
        
        # Create mass spectrum plot
        all_masses = []
        all_names = []
        colors = []
        
        color_map = {'Quarks': 'red', 'Leptons': 'blue', 'Bosons': 'green'}
        
        for particle_type, particle_dict in particles.items():
            for name, mass in particle_dict.items():
                if mass > 0:  # Only plot massive particles
                    all_masses.append(mass)
                    all_names.append(name)
                    colors.append(color_map[particle_type])
        
        # Sort by mass
        sorted_indices = np.argsort(all_masses)
        all_masses = [all_masses[i] for i in sorted_indices]
        all_names = [all_names[i] for i in sorted_indices]
        colors = [colors[i] for i in sorted_indices]
        
        y_positions = range(len(all_masses))
        
        axes[0].barh(y_positions, all_masses, color=colors, alpha=0.7)
        axes[0].set_yticks(y_positions)
        axes[0].set_yticklabels(all_names)
        axes[0].set_xlabel('Mass (GeV/c²)')
        axes[0].set_title('Particle Mass Spectrum')
        axes[0].set_xscale('log')
        axes[0].grid(True, alpha=0.3)
        
        # Add legend
        legend_elements = [plt.Rectangle((0,0),1,1, facecolor=color, alpha=0.7, 
                                       label=particle_type) 
                          for particle_type, color in color_map.items()]
        axes[0].legend(handles=legend_elements)
        
        # Coupling strength comparison
        interactions = {
            'Strong': 1,
            'Electromagnetic': 1/137,  # Fine structure constant
            'Weak': 10**(-6),
            'Gravitational': 10**(-39)
        }
        
        interaction_names = list(interactions.keys())
        strengths = list(interactions.values())
        
        axes[1].bar(interaction_names, strengths, 
                   color=['red', 'blue', 'green', 'purple'], alpha=0.7)
        axes[1].set_ylabel('Relative Coupling Strength')
        axes[1].set_title('Fundamental Interactions')
        axes[1].set_yscale('log')
        axes[1].grid(True, alpha=0.3)
        
        # Add strength values as text
        for i, (name, strength) in enumerate(interactions.items()):
            axes[1].text(i, strength * 2, f'{strength:.0e}', 
                        ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
        
    def cosmic_ray_shower_simulation(self):
        """Simulate cosmic ray air shower"""
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Primary cosmic ray parameters
        primary_energy = 10**15  # eV
        altitude = 30  # km
        
        # Simulate shower development
        def generate_shower(x0, y0, z0, energy, generation, max_gen=6):
            if generation >= max_gen or energy < 10**10:
                return [], [], [], []
            
            # Generate secondary particles
            n_secondaries = max(1, int(np.sqrt(energy/10**12)))
            n_secondaries = min(n_secondaries, 4)  # Limit for visualization
            
            x_particles, y_particles, z_particles, energies = [], [], [], []
            
            for i in range(n_secondaries):
                # Random directions (simplified)
                theta = np.random.normal(0, 0.1)  # Small angle scattering
                phi = np.random.uniform(0, 2*np.pi)
                
                # New position
                step_size = 5  # km
                dx = step_size * np.sin(theta) * np.cos(phi)
                dy = step_size * np.sin(theta) * np.sin(phi)
                dz = -step_size  # Downward
                
                x_new = x0 + dx
                y_new = y0 + dy
                z_new = z0 + dz
                
                # Energy sharing
                energy_fraction = np.random.beta(2, 2)
                new_energy = energy * energy_fraction / n_secondaries
                
                x_particles.append(x_new)
                y_particles.append(y_new)
                z_particles.append(z_new)
                energies.append(new_energy)
                
                # Draw line
                ax.plot([x0, x_new], [y0, y_new], [z0, z_new], 
                       'b-', alpha=0.6, linewidth=1)
                
                # Recursive call for next generation
                if z_new > 0:  # Above ground
                    x_next, y_next, z_next, e_next = generate_shower(
                        x_new, y_new, z_new, new_energy, generation + 1, max_gen)
                    x_particles.extend(x_next)
                    y_particles.extend(y_next)
                    z_particles.extend(z_next)
                    energies.extend(e_next)
            
            return x_particles, y_particles, z_particles, energies
        
        # Generate shower
        np.random.seed(42)
        x_shower, y_shower, z_shower, e_shower = generate_shower(
            0, 0, altitude, primary_energy, 0)
        
        # Plot primary cosmic ray
        ax.plot([0], [0], [altitude], 'ro', markersize=10, label='Primary CR')
        
        # Plot ground level detectors
        detector_x = np.linspace(-20, 20, 10)
        detector_y = np.linspace(-20, 20, 10)
        X_det, Y_det = np.meshgrid(detector_x, detector_y)
        Z_det = np.zeros_like(X_det)
        
        ax.plot_surface(X_det, Y_det, Z_det, alpha=0.3, color='brown')
        
        # Count particles at ground level
        ground_particles = [(x, y) for x, y, z in zip(x_shower, y_shower, z_shower) if abs(z) < 1]
        
        if ground_particles:
            gx, gy = zip(*ground_particles)
            ax.scatter(gx, gy, [0]*len(gx), c='red', s=20, alpha=0.8, label='Ground particles')
        
        ax.set_xlabel('X (km)')
        ax.set_ylabel('Y (km)')
        ax.set_zlabel('Altitude (km)')
        ax.set_title('Cosmic Ray Air Shower')
        ax.legend()
        
        plt.tight_layout()
        plt.show()
        
        return len(ground_particles)
        
    def run_all_visualizations(self):
        self.particle_decay_visualization()
        self.standard_model_visualization()
        shower_particles = self.cosmic_ray_shower_simulation()
        print(f"Cosmic ray shower produced {shower_particles} particles at ground level")

# Usage
particle_physics = ParticlePhysicsSimulator()
particle_physics.run_all_visualizations()