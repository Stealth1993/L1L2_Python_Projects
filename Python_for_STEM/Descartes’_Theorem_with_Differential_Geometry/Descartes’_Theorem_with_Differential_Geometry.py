import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Force a GUI backend if running in non-interactive environments
matplotlib.use('TkAgg')  # You can also try 'Qt5Agg' or comment this if using Jupyter

def generate_sphere(r):
    """Generate X, Y, Z coordinates for a sphere of radius r."""
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)
    
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    
    return x, y, z

def main():
    # Define radii for the spheres
    radii = [1, 2, 3, 4]
    colors = ['r', 'g', 'b', 'y']
    
    # Compute curvatures (1/r)
    curvatures = [1 / r for r in radii]
    total_curvature = sum(curvatures)

    # Create 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    for r, c in zip(radii, colors):
        x, y, z = generate_sphere(r)
        ax.plot_surface(x, y, z, color=c, alpha=0.5, rstride=5, cstride=5)

    # Set plot labels and title
    ax.set_title("Descartes' Theorem Visualization (Spheres & Curvature)", fontsize=14)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    # Annotate curvature
    ax.text2D(0.05, 0.95, f"Total Curvature: {total_curvature:.2f}", transform=ax.transAxes, fontsize=13)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()


# Description:# This code visualizes Descartes' Theorem using spheres in a 3D plot.
# It generates spheres of different radii, calculates their curvatures, and displays them interactively.
# The total curvature is also annotated on the plot.
# Descartes' Theorem with Differential Geometry
# This code visualizes Descartes' Theorem using spheres in a 3D plot.