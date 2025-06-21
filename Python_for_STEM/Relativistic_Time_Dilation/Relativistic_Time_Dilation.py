import numpy as np
import matplotlib.pyplot as plt 

# Parameters
v = np.linspace(0, 0.99 * 3e8, 1000) #Velocity m/s
c = 3e8 
t0 = 1.0 #Proper time(s)

# Lorentz factor
gamma = 1 / np.sqrt(1 - (v / c)**2)
t = t0 * gamma #Dialated time

# Plot
plt.figure(figsize=(10, 6))
plt.plot(v /c, t)
plt.title("Relativistic Time Dialation")
plt.xlabel("Velocity(v/c)")
plt.ylabel("Observer Time(s)")
plt.grid(True)
plt.show()