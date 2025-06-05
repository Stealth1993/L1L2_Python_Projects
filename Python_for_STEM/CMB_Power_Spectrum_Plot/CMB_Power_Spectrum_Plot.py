import numpy as np
import matplotlib.pyplot as plt
import camb
from astropy.cosmology import FlatLambdaCDM

# Cosmology
cosmo = FlatLambdaCDM(H0=70, Om0=0.3, Tcmb0=2.725)
pars = camb.CAMBparams()
pars.set_cosmology(H0=70, ombh2=0.022, omch2=0.122)
pars.InitPower.set_params(As=2e-9, ns=0.965)
pars.set_for_lmax(2500, lens_potential_accuracy=1)

# Calculate power spectrum
results = camb.get_results(pars)
powers = results.get_cmb_power_spectra(pars, CMB_unit='muK')
l = np.arange(2, 2501)

# Plot
plt.figure(figsize=(10, 6))
plt.loglog(l, powers['total'][2:2501, 0])
plt.title('CMB Temperature Power Spectrum')
plt.xlabel('Multipole (ℓ)')
plt.ylabel('C_ℓ (μK²)')
plt.legend()
plt.grid()
plt.show()

#This code generates a plot of the CMB temperature power spectrum using the CAMB package. The x-axis represents the multipole moment (ℓ), and the y-axis represents the power spectrum (C_ℓ) in units of μK². The plot is logarithmic on both axes to better visualize the range of values.
#The CMB power spectrum is a fundamental aspect of cosmology, providing insights into the early universe's conditions and the formation of large-scale structures. The parameters used in the code can be adjusted to explore different cosmological models and their effects on the CMB power spectrum.