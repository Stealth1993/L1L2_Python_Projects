import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

class ThermodynamicsVisualizer:
    def __init__(self):
        self.R = 8.314  # Gas constant
        self.k_B = 1.381e-23  # Boltzmann constant
        self.N_A = 6.022e23   # Avogadro's number