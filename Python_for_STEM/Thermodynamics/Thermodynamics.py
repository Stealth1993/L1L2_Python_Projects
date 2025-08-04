import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

class ThermodynamicsVisualizer:
    def __init__(self):
        self.R = 8.314  # Gas constant
        self.k_B = 1.381e-23  # Boltzmann constant
        self.N_A = 6.022e23   # Avogadro's number
        
    def ideal_gas_processes(self):
        """Visualize different thermodynamic processes"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Thermodynamic Processes', fontsize=16)
        
        # Initial state
        P1, V1, T1 = 1, 1, 300  # atm, L, K
        n = 1  # moles
        
        V = np.linspace(0.5, 3, 100)
        
        # Isothermal process (PV = constant)
        P_isothermal = P1 * V1 / V
        
        # Adiabatic process (PV^γ = constant)
        gamma = 1.4  # for diatomic gas
        P_adiabatic = P1 * (V1/V)**gamma
        
        # Isobaric process (P = constant)
        P_isobaric = np.full_like(V, P1)
        
        # Isochoric process (V = constant)
        V_isochoric = np.full(100, V1)
        P_isochoric = np.linspace(P1, 2*P1, 100)
        
        # P-V diagram
        axes[0,0].plot(V, P_isothermal, 'b-', linewidth=3, label='Isothermal')
        axes[0,0].plot(V, P_adiabatic, 'r-', linewidth=3, label='Adiabatic')
        axes[0,0].plot(V, P_isobaric, 'g-', linewidth=3, label='Isobaric')
        axes[0,0].plot(V_isochoric, P_isochoric, 'm-', linewidth=3, label='Isochoric')
        
        axes[0,0].set_title('P-V Diagram')
        axes[0,0].set_xlabel('Volume (L)')
        axes[0,0].set_ylabel('Pressure (atm)')
        axes[0,0].legend()
        axes[0,0].grid(True)
        
        # Maxwell-Boltzmann distribution
        T_values = [200, 300, 400, 500]  # Temperatures in K
        v = np.linspace(0, 1500, 1000)  # velocities in m/s
        m = 32e-3 / self.N_A  # mass of O2 molecule
        
        for T in T_values:
            f_v = 4*np.pi * (m/(2*np.pi*self.k_B*T))**(3/2) * v**2 * \
                  np.exp(-m*v**2/(2*self.k_B*T))
            axes[0,1].plot(v, f_v, linewidth=2, label=f'T = {T} K')
        
        axes[0,1].set_title('Maxwell-Boltzmann Distribution')
        axes[0,1].set_xlabel('Velocity (m/s)')
        axes[0,1].set_ylabel('f(v)')
        axes[0,1].legend()
        axes[0,1].grid(True)
        
        # Carnot cycle
        V_cycle = np.array([V1, 2*V1, 3*V1, 1.5*V1, V1])
        T_hot, T_cold = 400, 300
        
        # Isothermal expansion (hot)
        V_12 = np.linspace(V1, 2*V1, 25)
        P_12 = n*self.R*T_hot / V_12
        
        # Adiabatic expansion
        V_23 = np.linspace(2*V1, 3*V1, 25)
        P_23 = P_12[-1] * (V_23[0]/V_23)**gamma
        
        # Isothermal compression (cold)
        V_34 = np.linspace(3*V1, 1.5*V1, 25)
        P_34 = n*self.R*T_cold / V_34
        
        # Adiabatic compression
        V_41 = np.linspace(1.5*V1, V1, 25)
        P_41 = P_34[-1] * (V_41[0]/V_41)**gamma
        
        axes[1,0].plot(V_12, P_12, 'r-', linewidth=3, label='1→2: Isothermal (hot)')
        axes[1,0].plot(V_23, P_23, 'b-', linewidth=3, label='2→3: Adiabatic')
        axes[1,0].plot(V_34, P_34, 'g-', linewidth=3, label='3→4: Isothermal (cold)')
        axes[1,0].plot(V_41, P_41, 'orange', linewidth=3, label='4→1: Adiabatic')
        
        axes[1,0].set_title('Carnot Cycle')
        axes[1,0].set_xlabel('Volume')
        axes[1,0].set_ylabel('Pressure')
        axes[1,0].legend()
        axes[1,0].grid(True)
        
        # Entropy vs Temperature
        T_range = np.linspace(100, 500, 100)
        
        # Heat capacity (constant for ideal gas)
        Cv = 3/2 * self.R  # for monatomic gas
        Cp = 5/2 * self.R
        
        # Entropy (relative to reference state)
        S_V = n * Cv * np.log(T_range/T1)  # constant volume
        S_P = n * Cp * np.log(T_range/T1)  # constant pressure
        
        axes[1,1].plot(T_range, S_V, 'b-', linewidth=2, label='Constant Volume')
        axes[1,1].plot(T_range, S_P, 'r-', linewidth=2, label='Constant Pressure')
        
        axes[1,1].set_title('Entropy vs Temperature')
        axes[1,1].set_xlabel('Temperature (K)')
        axes[1,1].set_ylabel('Entropy Change (J/K)')
        axes[1,1].legend()
        axes[1,1].grid(True)
        
        plt.tight_layout()
        plt.show()
        
    def phase_diagrams(self):
        """Phase diagrams and transitions"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Phase Diagrams', fontsize=16)
        
        # Water phase diagram (schematic)
        T = np.linspace(250, 650, 1000)
        
        # Sublimation curve (solid-gas)
        P_sublimation = np.exp(25 - 6000/T)
        
        # Vaporization curve (liquid-gas)
        P_vaporization = np.exp(20 - 4000/T)
        
        # Melting curve (solid-liquid)
        P_melting = 1 + 0.01*(T - 273.15)
        
        ax1.semilogy(T, P_sublimation, 'b-', linewidth=3, label='Sublimation')
        ax1.semilogy(T, P_vaporization, 'r-', linewidth=3, label='Vaporization')
        ax1.semilogy(T, P_melting, 'g-', linewidth=3, label='Melting')
        
        # Triple point
        T_triple = 273.16
        P_triple = 611.657e-5  # bar
        ax1.plot(T_triple, P_triple, 'ko', markersize=8, label='Triple Point')
        
        # Critical point
        T_critical = 647.1
        P_critical = 220.64  # bar
        ax1.plot(T_critical, P_critical, 'ro', markersize=8, label='Critical Point')
        
        ax1.set_xlabel('Temperature (K)')
        ax1.set_ylabel('Pressure (bar)')
        ax1.set_title('Water Phase Diagram')
        ax1.legend()
        ax1.grid(True)
        
        # Fill phase regions
        ax1.fill_between([250, T_triple], [1e-6, 1e-6], [P_triple, P_triple], 
                        alpha=0.3, color='cyan', label='Solid')
        
        # Van der Waals equation of state
        V = np.linspace(0.1, 5, 1000)
        T_values = [0.9, 1.0, 1.1, 1.3]  # Reduced temperatures
        
        # Van der Waals parameters (reduced units)
        a, b = 1, 1/3
        
        for T_r in T_values:
            # Solve Van der Waals equation: (P + a/V²)(V - b) = T
            P_vdw = T_r/(V - b) - a/V**2
            
            # Only plot positive pressures
            valid_mask = (P_vdw > 0) & (V > b)
            ax2.plot(V[valid_mask], P_vdw[valid_mask], 
                    linewidth=2, label=f'T/Tc = {T_r}')
        
        ax2.set_xlabel('Reduced Volume (V/Vc)')
        ax2.set_ylabel('Reduced Pressure (P/Pc)')
        ax2.set_title('Van der Waals Isotherms')
        ax2.legend()
        ax2.grid(True)
        ax2.set_xlim(0.5, 5)
        ax2.set_ylim(0, 2)
        
        plt.tight_layout()
        plt.show()
        
    def run_all_visualizations(self):
        self.ideal_gas_processes()
        self.phase_diagrams()

# Usage
thermo_viz = ThermodynamicsVisualizer()
thermo_viz.run_all_visualizations()