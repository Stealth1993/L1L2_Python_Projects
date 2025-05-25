import numpy as np 
import matplotlib.pyplot as plt

# Generate a square wave signal
t = np.linspace(0, 1, 1000, endpoint=False)
square_wave = np.sign(np.sin(2 * np.pi * 5 * t))

# Perform FFT
fft_result = np.fft.fft(square_wave)

# Get Frequency bins
freqs = np.fft.fftfreq(len(square_wave), d=t[1]-t[0])

# Plot square wave and its FFT
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, square_wave, label='Square Wave', color='blue')
plt.title('Square Wave Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid()
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(freqs[:len(freqs)//2], np.abs(fft_result)[:len(fft_result)//2], label='FFT Magnitude', color='orange')
plt.title('FFT of Square Wave Signal')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()
# This code generates a square wave signal, computes its Fast Fourier Transform (FFT),
# and plots both the time-domain signal and its frequency-domain representation.