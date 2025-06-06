import numpy as np
import matplotlib.pyplot as plt 

# Parameters
N = 1000  # Number of points
x = np.linspace(0, 4, N)  # x values from 0 to 4

# Logistic map function
def logistic_map(r, x):
    return r * x * (1 - x)

# Initialize the bifurcation diagram
def bifurcation_diagram(r_min, r_max, num_r, num_iterations, last_points):
    r_values = np.linspace(r_min, r_max, num_r)
    x_values = np.zeros((num_r, last_points))
    
    for i, r in enumerate(r_values):
        x = 0.5  # Initial condition
        for _ in range(num_iterations):
            x = logistic_map(r, x)  # Iterate the logistic map
            if _ >= (num_iterations - last_points):  # Store last points
                x_values[i, _ - (num_iterations - last_points)] = x
    
    return r_values, x_values

# Plotting the bifurcation diagram
def plot_bifurcation_diagram(r_values, x_values):
    plt.figure(figsize=(10, 7))
    plt.plot(r_values, x_values, ',k', alpha=0.25)  # Plot points with small dots
    plt.title('Bifurcation Diagram of the Logistic Map')
    plt.xlabel('r (growth rate)')
    plt.ylabel('x (population)')
    plt.xlim(0, 4)
    plt.ylim(0, 1)
    plt.grid()
    plt.show()

# Main execution
if __name__ == "__main__":
    r_min = 2.5  # Minimum r value
    r_max = 4.0  # Maximum r value
    num_r = 1000  # Number of r values
    num_iterations = 1000  # Total iterations for each r
    last_points = 100  # Number of points to plot for each r

    r_values, x_values = bifurcation_diagram(r_min, r_max, num_r, num_iterations, last_points)
    plot_bifurcation_diagram(r_values, x_values)

# This code generates a bifurcation diagram for the logistic map.
# It visualizes how the population dynamics change with varying growth rates.
# The logistic map is a classic example of how complex behavior can arise from simple nonlinear dynamics.
# The bifurcation diagram shows the stable states of the system as a function of the growth rate.
# The code uses numpy for numerical calculations and matplotlib for plotting.
# The bifurcation diagram is a powerful tool in dynamical systems to visualize transitions between different behaviors.
# The code is structured to be modular, allowing for easy adjustments of parameters.

# Rabbit population dynamics can be modeled using the logistic map, which is a simple yet powerful model in chaos theory.
# The logistic map is defined as x_{n+1} = r * x_n * (1 - x_n), where r is the growth rate and x_n is the population at time n.