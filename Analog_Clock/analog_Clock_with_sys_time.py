import tkinter as tk
from math import sin, cos, pi
from datetime import datetime


def update_clock():
    # Fetch the current time
    now = datetime.now()
    seconds = now.second
    minutes = now.minute
    hours = now.hour % 12  # Convert to 12-hour format

    # Calculation of the angles for the clock hands (in degrees)
    seconds_angle = 90 - seconds * 6
    minutes_angle = 90 - minutes * 6 - seconds * 0.1
    hours_angle = 90 - (hours * 30 + minutes * 0.5)

    canvas.delete("all")  # Deletes all previous drawings

    # Draw the clock face
    canvas.create_oval(50, 50, 250, 250)  # Clock face border

    for i in range(1, 13):  # Draw the clock numbers
        angle = 90 - i * 30  # Angle for each number
        x = 150 + 85 * cos(angle * (pi / 180))
        y = 150 - 85 * sin(angle * (pi / 180))
        canvas.create_text(x, y, text=str(i), font=("Arial", 12, "bold"))

    # Draw the clock hands
    draw_hand(150, 150, seconds_angle, 80, 1)  # Second hand
    draw_hand(150, 150, minutes_angle, 70, 2)  # Minute hand
    draw_hand(150, 150, hours_angle, 50, 4)    # Hour hand

    # Schedule the next update
    root.after(1000, update_clock)  # Update the clock every 1000ms (1 second)


def draw_hand(x, y, angle, length, width):
    radian_angle = angle * (pi / 180)
    end_x = x + length * cos(radian_angle)
    end_y = y - length * sin(radian_angle)
    canvas.create_line(x, y, end_x, end_y, width=width)


# Main application window
root = tk.Tk()
root.title("Analog Clock")

canvas = tk.Canvas(root, width=350, height=350)
canvas.pack()

# Start updating the clock
update_clock()

# Run the Tkinter event loop
root.mainloop()
