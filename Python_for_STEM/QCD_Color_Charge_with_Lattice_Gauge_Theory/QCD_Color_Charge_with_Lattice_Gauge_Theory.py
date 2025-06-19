# this program is a simple example of how to use the QCD_Color_Charge_with_Lattice_Gauge_Theory module
# it will create a lattice gauge theory and calculate the color charge of a quark
import numpy as np
from QCD_Color_Charge_with_Lattice_Gauge_Theory import LatticeGaugeTheory, Quark
import matplotlib.pyplot as plt

# Create a lattice gauge theory with a 4x4x4x4 lattice
lattice_size = (4, 4, 4, 4)
lattice = LatticeGaugeTheory(lattice_size)

# Create a quark with a specific color charge
quark_color_charge = np.array([1, 0, 0])  # Red color charge
quark = Quark(color_charge=quark_color_charge)
# Add the quark to the lattice
lattice.add_quark(quark)
# Calculate the color charge of the quark
color_charge = lattice.calculate_color_charge(quark)
print(f"Color charge of the quark: {color_charge}")
# Visualize the lattice
lattice.visualize_lattice()
# Show the plot
plt.show()