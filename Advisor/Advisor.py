import requests
import threading
import tkinter as tk
from tkinter import messagebox

def fetch_advice():
    try:
        res = requests.get("https://api.adviceslip.com/advice").json()
        advice_text.set(res["slip"]["advice"])
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Failed to fetch advice. Check your internet.")

# Run API call in a separate thread
def advice():
    threading.Thread(target=fetch_advice, daemon=True).start()

# Copy advice text to clipboard
def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(advice_text.get())
    root.update()
    messagebox.showinfo("Copied", "Advice copied to clipboard!")

# GUI setup
root = tk.Tk()
root.title("Random Advisor Application")

advice_text = tk.StringVar()
tk.Label(root, textvariable=advice_text, wraplength=400, font=("Arial", 14)).pack(pady=20)

# Buttons
tk.Button(root, text="Get Advice", command=advice).pack(pady=5)
tk.Button(root, text="Copy Advice", command=copy_to_clipboard).pack(pady=5)

advice()  # Fetch initial advice
root.mainloop()

