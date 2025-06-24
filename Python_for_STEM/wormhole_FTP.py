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
button_fg = "#150303"     # Button text color
variable_fg = "#DADE74"   # Text color for status and messages

# Create main window
root = tk.Tk()
root.title("File Transfer using Magic Wormhole")
root.configure(bg=bg_color)
root.geometry("600x400")  # Slightly bigger window

# Create main frame
main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(expand=True, fill='both', padx=20, pady=20)

# Title label with 3D effect
title_label = tk.Label(main_frame, text="File Transfer", font=("Arial", 16), bg=bg_color, fg=text_color, relief='raised')
title_label.pack(pady=10)

# Button frame with 3D effect
button_frame = tk.Frame(main_frame, bg=bg_color, borderwidth=2, relief='groove')
button_frame.pack(pady=10)

# Buttons with 3D effect
send_file_button = tk.Button(button_frame, text="Send File", bg=button_bg, fg=button_fg, relief='raised', command=lambda: send_file())
send_file_button.grid(row=0, column=0, padx=5)

send_message_button = tk.Button(button_frame, text="Send Message", bg=button_bg, fg=button_fg, relief='raised', command=lambda: send_message())
send_message_button.grid(row=0, column=1, padx=5)

receive_button = tk.Button(button_frame, text="Receive", bg=button_bg, fg=button_fg, relief='raised', command=lambda: receive_file())
receive_button.grid(row=0, column=2, padx=5)

cancel_button = tk.Button(button_frame, text="Cancel", bg=button_bg, fg=button_fg, relief='raised', command=lambda: cancel_operation(), state=tk.DISABLED)
cancel_button.grid(row=0, column=3, padx=5)

# Status frame
status_frame = tk.Frame(main_frame, bg=bg_color)
status_frame.pack(pady=5)

status_label = tk.Label(status_frame, text="Ready", bg=bg_color, fg=variable_fg)
status_label.pack()

code_label = tk.Label(status_frame, text="", bg=bg_color, fg=variable_fg)
code_label.pack()

message_label = tk.Label(status_frame, text="", bg=bg_color, fg=variable_fg, wraplength=500, justify='left')
message_label.pack()

# QR frame
qr_frame = tk.Frame(main_frame, bg=bg_color)
qr_frame.pack(pady=5)

qr_label = tk.Label(qr_frame, bg=bg_color)
qr_label.pack()

# Bottom frame for Exit button
bottom_frame = tk.Frame(root, bg=bg_color)
bottom_frame.pack(side='bottom', fill='x')

exit_button = tk.Button(bottom_frame, text="Exit", bg=button_bg, fg=button_fg, relief='raised', command=root.quit)
exit_button.pack(pady=10)

# Queue for status updates and process tracking
status_queue = queue.Queue()
current_process = None

def send_file():
    """Initiate file sending process."""
    file_path = filedialog.askopenfilename()
    if file_path:
        status_label.config(text="Sending file...")
        send_file_button.config(state=tk.DISABLED)
        send_message_button.config(state=tk.DISABLED)
        receive_button.config(state=tk.DISABLED)
        cancel_button.config(state=tk.NORMAL)
        threading.Thread(target=send_thread, args=(file_path, None), daemon=True).start()

def send_message():
    """Initiate message sending process."""
    message = simpledialog.askstring("Send Message", "Enter the message to send:")
    if message:
        status_label.config(text="Sending message...")
        send_file_button.config(state=tk.DISABLED)
        send_message_button.config(state=tk.DISABLED)
        receive_button.config(state=tk.DISABLED)
        cancel_button.config(state=tk.NORMAL)
        threading.Thread(target=send_thread, args=(None, message), daemon=True).start()

def send_thread(file_path=None, message=None):
    """Handle sending files or messages in a separate thread."""
    global current_process
    try:
        if message:
            cmd = ["wormhole", "send", "--text", message]
        else:
            cmd = ["wormhole", "send", file_path]
        current_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in iter(current_process.stdout.readline, ''):
            line = line.strip()
            if "Wormhole code is:" in line:
                code = line.split(":", 1)[1].strip()
                status_queue.put(("code", code))
                # Generate and display QR code
                qr_img = qrcode.make(code)
                qr_img = qr_img.resize((200, 200), Image.Resampling.LANCZOS)
                qr_photo = ImageTk.PhotoImage(qr_img)
                status_queue.put(("qr", qr_photo))
        current_process.wait()
        if current_process.returncode == 0:
            status_queue.put(("done", "Send complete"))
        else:
            status_queue.put(("error", "Send failed"))
    except Exception as e:
        status_queue.put(("error", str(e)))

def receive_file():
    """Initiate file or message receiving process."""
    code = simpledialog.askstring("Receive", "Enter wormhole code:")
    if code:
        status_label.config(text="Receiving...")
        send_file_button.config(state=tk.DISABLED)
        send_message_button.config(state=tk.DISABLED)
        receive_button.config(state=tk.DISABLED)
        cancel_button.config(state=tk.NORMAL)
        threading.Thread(target=receive_thread, args=(code,), daemon=True).start()

def receive_thread(code):
    """Handle receiving files or messages in a separate thread."""
    global current_process
    try:
        current_process = subprocess.Popen(["wormhole", "receive", code], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        while True:
            line = current_process.stdout.readline()
            if not line:
                break
            line = line.strip()
            if "Receiving text message" in line:
                # Next line is "Message: <the message>"
                message_line = current_process.stdout.readline().strip()
                if message_line.startswith("Message: "):
                    message = message_line[len("Message: "):]
                    status_queue.put(("message", message))
            elif "ok? (y/n):" in line:
                # Automatically accept the file
                current_process.stdin.write('y\n')
                current_process.stdin.flush()
        current_process.wait()
        if current_process.returncode == 0:
            status_queue.put(("done", "Receive complete"))
        else:
            status_queue.put(("error", "Receive failed"))
    except Exception as e:
        status_queue.put(("error", str(e)))

def cancel_operation():
    """Cancel any ongoing file or message transfer operation."""
    global current_process
    if current_process:
        current_process.terminate()
        status_label.config(text="Cancelled")
        send_file_button.config(state=tk.NORMAL)
        send_message_button.config(state=tk.NORMAL)
        receive_button.config(state=tk.NORMAL)
        cancel_button.config(state=tk.DISABLED)
        code_label.config(text="")
        qr_label.config(image="")
        message_label.config(text="")

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
            elif msg[0] == "message":
                message_label.config(text=f"Received message: {msg[1]}")
            elif msg[0] == "done":
                status_label.config(text=msg[1])
                send_file_button.config(state=tk.NORMAL)
                send_message_button.config(state=tk.NORMAL)
                receive_button.config(state=tk.NORMAL)
                cancel_button.config(state=tk.DISABLED)
                code_label.config(text="")
                qr_label.config(image="")
                message_label.config(text="")
            elif msg[0] == "error":
                messagebox.showerror("Error", msg[1])
                status_label.config(text="Error")
                send_file_button.config(state=tk.NORMAL)
                send_message_button.config(state=tk.NORMAL)
                receive_button.config(state=tk.NORMAL)
                cancel_button.config(state=tk.DISABLED)
                code_label.config(text="")
                qr_label.config(image="")
                message_label.config(text="")
    except queue.Empty:
        pass
    root.after(100, check_queue)

# Start checking the queue
root.after(100, check_queue)

# Run the main loop
root.mainloop()