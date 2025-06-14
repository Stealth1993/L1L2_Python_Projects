import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.integrate import odeint
import matplotlib.animation as animation

# Constants
G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
AU = 1.495978707e11  # 1 AU in meters
C = 3.0e8  # Speed of light in m/s

# Derivatives function for n-body system
def derivatives(state, t, m, n, use_gr, gr_factor):
    positions = state[:2*n]
    velocities = state[2*n:]
    accelerations = np.zeros(2*n)
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = positions[2*j] - positions[2*i]
                dy = positions[2*j+1] - positions[2*i+1]
                r = np.sqrt(dx**2 + dy**2)
                if r > 0:
                    # Newtonian acceleration
                    a_newton = G * m[j] / r**3
                    accelerations[2*i] += a_newton * dx
                    accelerations[2*i+1] += a_newton * dy
                    # GR correction (simplified post-Newtonian term)
                    if use_gr and gr_factor > 0:
                        gamma = gr_factor * (G * m[j]) / (C**2 * r)
                        a_gr = a_newton * gamma
                        accelerations[2*i] += a_gr * dx
                        accelerations[2*i+1] += a_gr * dy
    return np.concatenate([velocities, accelerations])

class NBodyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive N-Body Simulation")

        # Variables to store animation state
        self.ani = None
        self.running = False

        # Number of bodies
        self.n_label = tk.Label(root, text="Number of Bodies (1-5):")
        self.n_label.pack()
        self.n_var = tk.IntVar(value=2)
        self.n_var.trace("w", self.update_inputs)
        self.n_spin = tk.Spinbox(root, from_=1, to=5, textvariable=self.n_var)
        self.n_spin.pack()

        # Input fields for masses, positions, and velocities
        self.mass_entries = []
        self.pos_entries = []
        self.vel_entries = []
        self.input_frame = tk.Frame(root)
        self.input_frame.pack()

        # GR toggle and factor
        self.gr_frame = tk.Frame(root)
        self.gr_frame.pack()
        self.use_gr_var = tk.BooleanVar(value=False)
        self.gr_check = tk.Checkbutton(self.gr_frame, text="Use GR Approximation", variable=self.use_gr_var, command=self.update_simulation)
        self.gr_check.pack(side=tk.LEFT)
        self.gr_factor_label = tk.Label(self.gr_frame, text="GR Factor:")
        self.gr_factor_label.pack(side=tk.LEFT)
        self.gr_factor_var = tk.StringVar(value="1000")  # Exaggerated for visibility
        self.gr_factor_var.trace("w", self.update_simulation)
        self.gr_factor_entry = tk.Entry(self.gr_frame, textvariable=self.gr_factor_var, width=10)
        self.gr_factor_entry.pack(side=tk.LEFT)

        # Total time and num frames
        self.time_label = tk.Label(root, text="Total Time (s):")
        self.time_label.pack()
        self.time_var = tk.StringVar(value="1e7")
        self.time_var.trace("w", self.update_simulation)
        self.time_entry = tk.Entry(root, textvariable=self.time_var)
        self.time_entry.pack()

        self.frames_label = tk.Label(root, text="Number of Frames:")
        self.frames_label.pack()
        self.frames_var = tk.StringVar(value="500")
        self.frames_var.trace("w", self.update_simulation)
        self.frames_entry = tk.Entry(root, textvariable=self.frames_var)
        self.frames_entry.pack()

        # Prediction inputs
        self.predict_label = tk.Label(root, text="Future Time (s):")
        self.predict_label.pack()
        self.predict_var = tk.StringVar(value="1e7")
        self.predict_entry = tk.Entry(root, textvariable=self.predict_var)
        self.predict_entry.pack()

        self.predict_button = tk.Button(root, text="Predict Positions", command=self.predict_positions)
        self.predict_button.pack()

        # Output text
        self.output_text = tk.Text(root, height=10, width=50)
        self.output_text.pack()

        # Figure for animation
        self.fig = Figure(figsize=(5, 5))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # Initial setup
        self.update_inputs()

    def update_inputs(self, *args):
        # Clear previous inputs
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        n = self.n_var.get()
        self.mass_entries = []
        self.pos_entries = []
        self.vel_entries = []

        # Create new input fields
        for i in range(n):
            label = tk.Label(self.input_frame, text=f"Body {i+1}:")
            label.grid(row=i, column=0)
            mass_label = tk.Label(self.input_frame, text="Mass (kg):")
            mass_label.grid(row=i, column=1)
            mass_var = tk.StringVar(value="1e30" if i == 0 else "1e24")
            mass_var.trace("w", self.update_simulation)
            mass_entry = tk.Entry(self.input_frame, textvariable=mass_var)
            mass_entry.grid(row=i, column=2)
            self.mass_entries.append(mass_entry)
            
            pos_label = tk.Label(self.input_frame, text="x (AU):")
            pos_label.grid(row=i, column=3)
            x_var = tk.StringVar(value="0" if i == 0 else "1")
            x_var.trace("w", self.update_simulation)
            x_entry = tk.Entry(self.input_frame, textvariable=x_var)
            x_entry.grid(row=i, column=4)
            
            pos_label_y = tk.Label(self.input_frame, text="y (AU):")
            pos_label_y.grid(row=i, column=5)
            y_var = tk.StringVar(value="0")
            y_var.trace("w", self.update_simulation)
            y_entry = tk.Entry(self.input_frame, textvariable=y_var)
            y_entry.grid(row=i, column=6)
            self.pos_entries.append((x_entry, y_entry))
            
            vel_label = tk.Label(self.input_frame, text="vx (m/s):")
            vel_label.grid(row=i, column=7)
            vx_var = tk.StringVar(value="0")
            vx_var.trace("w", self.update_simulation)
            vx_entry = tk.Entry(self.input_frame, textvariable=vx_var)
            vx_entry.grid(row=i, column=8)
            
            vel_label_y = tk.Label(self.input_frame, text="vy (m/s):")
            vel_label_y.grid(row=i, column=9)
            vy_var = tk.StringVar(value="0" if i == 0 else "2.11e4" if i == 1 and n == 2 else "0")
            vy_var.trace("w", self.update_simulation)
            vy_entry = tk.Entry(self.input_frame, textvariable=vy_var)
            vy_entry.grid(row=i, column=10)
            self.vel_entries.append((vx_entry, vy_entry))

        self.update_simulation()

    def get_parameters(self):
        try:
            n = self.n_var.get()
            m = [float(entry.get()) for entry in self.mass_entries]
            initial_positions = []
            for x_entry, y_entry in self.pos_entries:
                x = float(x_entry.get()) * AU
                y = float(y_entry.get()) * AU
                initial_positions.extend([x, y])
            initial_velocities = []
            for vx_entry, vy_entry in self.vel_entries:
                vx = float(vx_entry.get())
                vy = float(vy_entry.get())
                initial_velocities.extend([vx, vy])
            total_time = float(self.time_var.get())
            num_frames = int(self.frames_var.get())
            use_gr = self.use_gr_var.get()
            gr_factor = float(self.gr_factor_var.get())
            return n, m, initial_positions, initial_velocities, total_time, num_frames, use_gr, gr_factor
        except ValueError:
            return None

    def update_simulation(self, *args):
        if self.ani is not None:
            self.ani.event_source.stop()
            self.running = False

        params = self.get_parameters()
        if params is None:
            return

        n, m, initial_positions, initial_velocities, total_time, num_frames, use_gr, gr_factor = params
        initial_state = np.array(initial_positions + initial_velocities)

        times = np.linspace(0, total_time, num_frames)
        sol = odeint(derivatives, initial_state, times, args=(m, n, use_gr, gr_factor))

        self.ax.clear()
        x_all = sol[:, 0:2*n:2] / AU
        y_all = sol[:, 1:2*n:2] / AU
        self.ax.set_xlim(np.min(x_all) * 1.1, np.max(x_all) * 1.1)
        self.ax.set_ylim(np.min(y_all) * 1.1, np.max(y_all) * 1.1)
        self.ax.set_xlabel("x (AU)")
        self.ax.set_ylabel("y (AU)")
        title = "N-Body Simulation (Newtonian)" if not use_gr else "N-Body Simulation (GR Approx)"
        self.ax.set_title(title)
        self.ax.grid(True)

        scatter = self.ax.scatter(x_all[0], y_all[0], c=np.arange(n), cmap='tab10', s=50)

        def update(frame):
            scatter.set_offsets(np.c_[x_all[frame], y_all[frame]])
            return scatter,

        self.ani = animation.FuncAnimation(self.fig, update, frames=num_frames, interval=50, blit=True, repeat=True)
        self.running = True
        self.canvas.draw()

    def predict_positions(self):
        params = self.get_parameters()
        if params is None:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Invalid input parameters.\n")
            return

        n, m, initial_positions, initial_velocities, _, _, use_gr, gr_factor = params
        initial_state = np.array(initial_positions + initial_velocities)
        try:
            t_future = float(self.predict_var.get())
        except ValueError:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Invalid future time.\n")
            return

        sol = odeint(derivatives, initial_state, [0, t_future], args=(m, n, use_gr, gr_factor))
        positions = sol[-1, :2*n].reshape(n, 2) / AU

        output = f"Positions at t = {t_future} s ({'Newtonian' if not use_gr else 'GR Approx'}):\n"
        for i in range(n):
            output += f"Body {i+1}: x = {positions[i,0]:.2f} AU, y = {positions[i,1]:.2f} AU\n"
        output += "\nRelative distances:\n"
        for i in range(n):
            for j in range(i+1, n):
                dx = positions[i,0] - positions[j,0]
                dy = positions[i,1] - positions[j,1]
                dist = np.sqrt(dx**2 + dy**2)
                output += f"Body {i+1} - Body {j+1}: {dist:.2f} AU\n"
        if use_gr:
            output += "\nGR Note: Precession exaggerated by factor for visibility.\n"
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, output)

# Create and run the GUI
root = tk.Tk()
app = NBodyGUI(root)
root.mainloop()