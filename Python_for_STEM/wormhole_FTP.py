import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import threading
import queue
import subprocess
import qrcode
from PIL import Image, ImageTk

# Color definitions
bg_color = "#050608"      # Dark background
text_color = "#f00487"    # Pink text
button_bg = "#A4C639"     # Android Green for buttons
button_fg = "#ffffff"     # White text on buttons

# Create main window
root = tk.Tk()
root.title("File Transfer using Magic Wormhole")
root.configure(bg=bg_color)

# Create widgets
title_label = tk.Label(root, text="File Transfer", font=("Arial", 16), bg=bg_color, fg=text_color)
title_label.pack(pady=10)

button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=10)

send_button = tk.Button(button_frame, text="Send", bg=button_bg, fg=button_fg, command=lambda: send_file())
send_button.grid(row=0, column=0, padx=5)

receive_button = tk.Button(button_frame, text="Receive", bg=button_bg, fg=button_fg, command=lambda: receive_file())
receive_button.grid(row=0, column=1, padx=5)

cancel_button = tk.Button(button_frame, text="Cancel", bg=button_bg, fg=button_fg, command=lambda: cancel_operation(), state=tk.DISABLED)
cancel_button.grid(row=0, column=2, padx=5)

exit_button = tk.Button(button_frame, text="Exit", bg=button_bg, fg=button_fg, command=root.quit)
exit_button.grid(row=0, column=3, padx=5)

status_label = tk.Label(root, text="Ready", bg=bg_color, fg=text_color)
status_label.pack(pady=5)

code_label = tk.Label(root, text="", bg=bg_color, fg=text_color)
code_label.pack(pady=5)

qr_label = tk.Label(root, bg=bg_color)
qr_label.pack(pady=5)

# Queue for status updates and process tracking
status_queue = queue.Queue()
current_process = None

def send_file():
    """Initiate file sending process."""
    file_path = filedialog.askopenfilename()
    if file_path:
        status_label.config(text="Sending...")
        send_button.config(state=tk.DISABLED)
        receive_button.config(state=tk.DISABLED)
        cancel_button.config(state=tk.NORMAL)
        threading.Thread(target=send_thread, args=(file_path,), daemon=True).start()

def send_thread(file_path):
    """Handle file sending in a separate thread."""
    global current_process
    try:
        current_process = subprocess.Popen(["wormhole", "send", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in current_process.stdout:
            if "Wormhole code is:" in line:
                code = line.split(":")[1].strip()
                status_queue.put(("code", code))
                # Generate and display QR code
                qr_img = qrcode.make(code)
                qr_img = qr_img.resize((200, 200), Image.Resampling.LANCZOS)
                qr_photo = ImageTk.PhotoImage(qr_img)
                status_queue.put(("qr", qr_photo))
            # Continue reading until the process ends
        current_process.wait()
        if current_process.returncode == 0:
            status_queue.put(("done", "Send complete"))
        else:
            error_output = current_process.stderr.read()
            status_queue.put(("error", "Send failed: " + error_output))
    except Exception as e:
        status_queue.put(("error", str(e)))

def receive_file():
    """Initiate file receiving process."""
    code = simpledialog.askstring("Receive", "Enter wormhole code:")
    if code:
        status_label.config(text="Receiving...")
        send_button.config(state=tk.DISABLED)
        receive_button.config(state=tk.DISABLED)
        cancel_button.config(state=tk.NORMAL)
        threading.Thread(target=receive_thread, args=(code,), daemon=True).start()

def receive_thread(code):
    """Handle file receiving in a separate thread."""
    global current_process
    try:
        current_process = subprocess.Popen(["wormhole", "receive", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in current_process.stdout:
            pass  # Read output to prevent blocking
        current_process.wait()
        if current_process.returncode == 0:
            status_queue.put(("done", "Receive complete"))
        else:
            error_output = current_process.stderr.read()
            status_queue.put(("error", "Receive failed: " + error_output))
    except Exception as e:
        status_queue.put(("error", str(e)))

def cancel_operation():
    """Cancel any ongoing file transfer operation."""
    global current_process
    if current_process:
        current_process.terminate()
        status_label.config(text="Cancelled")
        send_button.config(state=tk.NORMAL)
        receive_button.config(state=tk.NORMAL)
        cancel_button.config(state=tk.DISABLED)
        code_label.config(text="")
        qr_label.config(image="")

def check_queue():
    """Check the queue for updates and refresh the GUI."""
    try:
        while True:
            msg = status_queue.get_nowait()
            if msg[0] == "code":
                code_label.config(text=f"Code: {msg[1]}")
            elif msg[0] == "qr":
                qr_label.config(image=msg[1])
                qr_label.image = msg[1]  # Keep reference to avoid garbage collection
            elif msg[0] == "done":
                status_label.config(text=msg[1])
                send_button.config(state=tk.NORMAL)
                receive_button.config(state=tk.NORMAL)
                cancel_button.config(state=tk.DISABLED)
                code_label.config(text="")
                qr_label.config(image="")
            elif msg[0] == "error":
                messagebox.showerror("Error", msg[1])
                status_label.config(text="Error")
                send_button.config(state=tk.NORMAL)
                receive_button.config(state=tk.NORMAL)
                cancel_button.config(state=tk.DISABLED)
    except queue.Empty:
        pass
    root.after(100, check_queue)

# Start checking the queue
root.after(100, check_queue)

# Run the main loop
root.mainloop()