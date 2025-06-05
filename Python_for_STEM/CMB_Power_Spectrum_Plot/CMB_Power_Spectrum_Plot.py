import numpy as np
import matplotlib.pyplot as plt 
from astropy.cosmology import Planck18 as cosmo
from astropy import units as u
import camb

# Cosmological parameters
H0 = 67.4  # Hubble constant in km/s/Mpc
ombh2 = 0.0224  # Baryon density parameter
omch2 = 0.1198  # Cold dark matter density parameter
omk = 0.0  # Curvature density parameter
tau = 0.054  # Optical depth to reionization
# Neutrino parameters
Nnu = 3.046  # Effective number of neutrino species
mnu = 0.06  # Total neutrino mass in eV
# Create a CAMB cosmology object
params = camb.CAMBparams()
params.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, omk=omk, tau=tau)
params.set_dark_energy(w=-1.0, wa=0.0)  # Dark energy parameters
params.f_SetNeutrinoHierarchy('normal')  # Neutrino hierarchy
params.set_nnu(Nnu)  # Effective number of neutrino species
params.set_mnu(mnu)  # Total neutrino mass
# Set the redshift range for the CMB power spectrum
params.set_redshift(0.0, 10.0)  # From z=0 to z=10
# Set the maximum multipole moment
params.set_max_l(2500)  # Maximum multipole moment
# Calculate the CMB power spectrum
results = camb.get_results(params)
# Get the CMB power spectrum
cls = results.get_cmb_power_spectra(params, CMB_unit='muK')
# Extract the temperature power spectrum
l = np.arange(len(cls['total'][:, 0]))
cl_tt = cls['total'][:, 0]  # Temperature power spectrum
# Plot the CMB power spectrum
plt.figure(figsize=(10, 6))
plt.plot(l, cl_tt, label='CMB Temperature Power Spectrum', color='blue')
plt.xlabel('Multipole Moment (l)')
plt.ylabel('C_l (μK^2)')
plt.title('CMB Temperature Power Spectrum')
plt.legend()
plt.grid()
plt.show()