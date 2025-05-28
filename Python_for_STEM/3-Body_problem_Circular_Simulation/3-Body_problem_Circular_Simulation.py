import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
AU = 1.495978707e11  # 1 AU in meters

class NBodySimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive N-Body Simulation")

        # Create frames for side-by-side layout
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        # Number of bodies
        self.n = 3  # Central body + 2 orbiting bodies
        self.masses = [1.989e30, 5.972e24, 1.898e27]  # Sun, Earth, Jupiter (kg)
        self.positions = np.array([[0.0, 0.0], [1.0, 0.0], [5.2, 0.0]])  # AU
        self.velocities = self.calculate_initial_velocities()

        # GUI Elements
        self.create_widgets()

        # Simulation Parameters
        self.num_frames = 500  # Enough frames for smooth animation
        self.total_time = self.calculate_total_time()
        self.times = np.linspace(0, self.total_time, self.num_frames)

        # Animation Parameters
        self.interval = 50  # Initial interval in ms
        self.min_interval = 10
        self.max_interval = 200
        self.interval_step = 10

        # Figure and Axes for Plotting
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_xlim(-6, 6)
        self.ax.set_ylim(-6, 6)
        self.ax.set_xlabel("x (AU)")
        self.ax.set_ylabel("y (AU)")
        self.ax.set_title("N-Body Simulation")
        self.ax.grid(True)

        # Scatter Plot
        self.scatter = self.ax.scatter(self.positions[:, 0], self.positions[:, 1], 
                                     c=np.arange(self.n), cmap='tab10', s=50)

        # Embed Plot in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Animation Object
        self.ani = None

        # Bind window close event to exit_application
        self.root.protocol("WM_DELETE_WINDOW", self.exit_application)

    def create_widgets(self):
        # Sliders for masses and entries for positions
        self.mass_sliders = []
        self.pos_x_entries = []
        self.pos_y_entries = []

        for i in range(self.n):
            # Mass Slider
            mass_label = tk.Label(self.input_frame, text=f"Mass {i+1} (kg):")
            mass_label.pack()
            mass_slider = tk.Scale(self.input_frame, from_=1e24, to=1e30, 
                                 orient=tk.HORIZONTAL, length=300)
            mass_slider.set(self.masses[i])
            mass_slider.pack()
            self.mass_sliders.append(mass_slider)

            # Position Entries
            pos_x_label = tk.Label(self.input_frame, text=f"Initial x {i+1} (AU):")
            pos_x_label.pack()
            pos_x_entry = tk.Entry(self.input_frame)
            pos_x_entry.insert(0, str(self.positions[i, 0]))
            pos_x_entry.pack()
            self.pos_x_entries.append(pos_x_entry)

            pos_y_label = tk.Label(self.input_frame, text=f"Initial y {i+1} (AU):")
            pos_y_label.pack()
            pos_y_entry = tk.Entry(self.input_frame)
            pos_y_entry.insert(0, str(self.positions[i, 1]))
            pos_y_entry.pack()
            self.pos_y_entries.append(pos_y_entry)

        # Buttons
        self.update_button = tk.Button(self.input_frame, text="Update Simulation", 
                                     command=self.update_simulation)
        self.update_button.pack()

        self.animate_button = tk.Button(self.input_frame, text="Start Animation", 
                                      command=self.start_animation)
        self.animate_button.pack()

        self.predict_button = tk.Button(self.input_frame, text="Predict Future Positions", 
                                      command=self.predict_positions)
        self.predict_button.pack()

        # Speed Control Buttons
        self.speed_up_button = tk.Button(self.input_frame, text="Speed Up", 
                                       command=self.speed_up)
        self.speed_up_button.pack()

        self.slow_down_button = tk.Button(self.input_frame, text="Slow Down", 
                                        command=self.slow_down)
        self.slow_down_button.pack()

        # Exit Button
        self.exit_button = tk.Button(self.input_frame, text="Exit", 
                                   command=self.exit_application)
        self.exit_button.pack()

    def calculate_initial_velocities(self):
        """Calculate initial velocities for circular orbits."""
        velocities = np.zeros((self.n, 2))
        central_mass = self.masses[0]
        for i in range(1, self.n):
            r = np.sqrt(self.positions[i, 0]**2 + self.positions[i, 1]**2) * AU
            v = np.sqrt(G * central_mass / r)  # Circular orbit velocity
            angle = np.arctan2(self.positions[i, 1], self.positions[i, 0])
            velocities[i, 0] = -v * np.sin(angle) / AU
            velocities[i, 1] = v * np.cos(angle) / AU
        return velocities

    def calculate_total_time(self):
        """Calculate total simulation time based on the farthest body's orbital period."""
        farthest_body = np.argmax([np.sqrt(p[0]**2 + p[1]**2) 
                                 for p in self.positions[1:]]) + 1
        r = np.sqrt(self.positions[farthest_body, 0]**2 + 
                   self.positions[farthest_body, 1]**2) * AU
        T = 2 * np.pi * np.sqrt(r**3 / (G * self.masses[0]))
        return T  # Time for one full orbit

    def update_simulation(self):
        """Update simulation parameters from GUI inputs."""
        # Update masses and positions
        for i in range(self.n):
            self.masses[i] = float(self.mass_sliders[i].get())
            self.positions[i, 0] = float(self.pos_x_entries[i].get())
            self.positions[i, 1] = float(self.pos_y_entries[i].get())

        # Recalculate velocities and total time
        self.velocities = self.calculate_initial_velocities()
        self.total_time = self.calculate_total_time()
        self.times = np.linspace(0, self.total_time, self.num_frames)

        # Update scatter plot
        self.scatter.set_offsets(self.positions)
        self.canvas.draw()

    def derivatives(self, state, t):
        """Compute derivatives for the ODE solver."""
        positions = state[:2*self.n].reshape(self.n, 2)
        velocities = state[2*self.n:].reshape(self.n, 2)
        accelerations = np.zeros_like(positions)
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    dx = positions[j, 0] - positions[i, 0]
                    dy = positions[j, 1] - positions[i, 1]
                    r = np.sqrt(dx**2 + dy**2)
                    if r > 0:
                        accelerations[i, 0] += G * self.masses[j] * dx / r**3
                        accelerations[i, 1] += G * self.masses[j] * dy / r**3
        return np.concatenate([velocities.flatten(), accelerations.flatten()])

    def start_animation(self):
        """Start or restart the animation."""
        if self.ani is not None:
            self.ani.event_source.stop()

        # Initial state in meters
        initial_positions_m = self.positions * AU
        initial_velocities_m = self.velocities * AU
        initial_state = np.concatenate([initial_positions_m.flatten(), 
                                      initial_velocities_m.flatten()])

        # Solve ODE
        sol = odeint(self.derivatives, initial_state, self.times)
        x_all = sol[:, 0:2*self.n:2] / AU
        y_all = sol[:, 1:2*self.n:2] / AU

        # Animation function
        def update(frame):
            self.scatter.set_offsets(np.c_[x_all[frame], y_all[frame]])
            return self.scatter,

        # Create animation
        self.ani = FuncAnimation(self.fig, update, frames=self.num_frames, 
                               interval=self.interval, blit=True)
        self.canvas.draw()

    def predict_positions(self):
        """Predict positions at a future time."""
        t_future = float(input("Enter future time (seconds): "))
        initial_state = np.concatenate([self.positions.flatten() * AU, 
                                      self.velocities.flatten() * AU])
        sol = odeint(self.derivatives, initial_state, [0, t_future])
        positions_m = sol[-1, :2*self.n].reshape(self.n, 2)
        positions_au = positions_m / AU

        # Output positions
        print(f"\nPositions at t = {t_future} seconds:")
        for i in range(self.n):
            print(f"Body {i+1}: x = {positions_au[i,0]:.2f} AU, y = {positions_au[i,1]:.2f} AU")

        # Output relative distances
        print("\nRelative distances:")
        for i in range(self.n):
            for j in range(i+1, self.n):
                dx = positions_au[i,0] - positions_au[j,0]
                dy = positions_au[i,1] - positions_au[j,1]
                dist = np.sqrt(dx**2 + dy**2)
                print(f"Distance between Body {i+1} and Body {j+1}: {dist:.2f} AU")

    def speed_up(self):
        """Increase animation speed."""
        if self.interval > self.min_interval:
            self.interval -= self.interval_step
            self.start_animation()
            print(f"Animation speed increased. Current interval: {self.interval} ms")

    def slow_down(self):
        """Decrease animation speed."""
        if self.interval < self.max_interval:
            self.interval += self.interval_step
            self.start_animation()
            print(f"Animation speed decreased. Current interval: {self.interval} ms")

    def exit_application(self):
        """Exit the application cleanly."""
        if self.ani is not None:
            self.ani.event_source.stop()
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NBodySimulation(root)
    root.mainloop()

# This code creates an interactive N-body simulation using Tkinter for the GUI and Matplotlib for visualization.
# Users can adjust masses and initial positions of celestial bodies, start an animation, and predict future positions.
# The simulation uses the gravitational force to calculate the motion of the bodies over time.