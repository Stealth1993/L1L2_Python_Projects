import os
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x400")

        # Flag to track if a download is in progress
        self.downloading = False

        # URL Label and Entry
        self.url_label = tk.Label(root, text="YouTube URL:")
        self.url_label.grid(row=0, column=0, padx=10, pady=10)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        # Type Dropdown
        self.type_label = tk.Label(root, text="Download Type:")
        self.type_label.grid(row=1, column=0, padx=10, pady=10)
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(root, textvariable=self.type_var, values=["Video with Audio", "Audio Only", "Video Only"])
        self.type_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.type_dropdown.bind("<<ComboboxSelected>>", self.update_quality_options)

        # Quality Dropdown
        self.quality_label = tk.Label(root, text="Quality:")
        self.quality_label.grid(row=2, column=0, padx=10, pady=10)
        self.quality_var = tk.StringVar()
        self.quality_dropdown = ttk.Combobox(root, textvariable=self.quality_var)
        self.quality_dropdown.grid(row=2, column=1, padx=10, pady=10)

        # Destination Label and Entry
        self.dest_label = tk.Label(root, text="Download Destination:")
        self.dest_label.grid(row=3, column=0, padx=10, pady=10)
        self.dest_entry = tk.Entry(root, width=50)
        self.dest_entry.grid(row=3, column=1, padx=10, pady=10)
        self.dest_entry.insert(0, self.get_default_download_path())
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_destination)
        self.browse_button.grid(row=3, column=2, padx=10, pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", style="green.Horizontal.TProgressbar")
        self.progress.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        # Status Label
        self.status_label = tk.Label(root, text="")
        self.status_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Download Button
        self.download_button = tk.Button(root, text="Download", command=self.start_download)
        self.download_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Exit Button
        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.grid(row=6, column=2, padx=10, pady=10)

        # Configure green progress bar style
        style = ttk.Style()
        style.configure("green.Horizontal.TProgressbar", troughcolor='gray', background='green')

    def get_default_download_path(self):
        return os.path.join(os.path.expanduser("~"), "Downloads\\YouTubeDownloads")

    def browse_destination(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, folder)

    def update_quality_options(self, event=None):
        type_selected = self.type_var.get()
        if type_selected == "Video with Audio":
            self.quality_dropdown['values'] = ["144p", "240p", "360p", "480p", "720p", "1080p"]
        elif type_selected == "Audio Only":
            self.quality_dropdown['values'] = ["64kbps", "128kbps", "192kbps", "256kbps"]
        elif type_selected == "Video Only":
            self.quality_dropdown['values'] = ["144p", "240p", "360p", "480p", "720p", "1080p"]
        self.quality_var.set("")

    def start_download(self):
        if self.downloading:
            messagebox.showinfo("Info", "A download is already in progress. Please wait.")
            return

        # Set downloading flag and disable button
        self.downloading = True
        self.download_button.config(state=tk.DISABLED)
        self.status_label.config(text="Preparing download...")

        # Start download in a new thread
        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()

    def download_video(self):
        url = self.url_entry.get()
        type_selected = self.type_var.get()
        quality_selected = self.quality_var.get()
        output_path = self.dest_entry.get()

        if not url or not type_selected or not quality_selected:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            self.reset_download_state()
            return

        # Unique output template with timestamp to prevent overwrites
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s_{timestamp}.%(ext)s',
            'progress_hooks': [self.progress_hook],
            'quiet': False,
            'nopart': False,  # Allow .part files during download, renamed on completion
            'retries': 10,    # Retry on failure to ensure completion
        }

        # Configure download options based on type and quality
        if type_selected == "Video with Audio":
            ydl_opts['format'] = f'bestvideo[height<={quality_selected[:-1]}]+bestaudio/best[height<={quality_selected[:-1]}]'
            ydl_opts['merge_output_format'] = 'mp4'
        elif type_selected == "Audio Only":
            ydl_opts['format'] = 'bestaudio'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality_selected[:-4],
            }]
        elif type_selected == "Video Only":
            ydl_opts['format'] = f'bestvideo[height<={quality_selected[:-1]}]'
            ydl_opts['merge_output_format'] = 'mp4'

        # Reset UI elements
        self.progress['value'] = 0
        self.status_label.config(text="Starting download...")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.root.after(0, self.status_label.config, {"text": "Download completed successfully!"})
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Download Error", f"An error occurred: {e}")
        finally:
            self.reset_download_state()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            if '_percent_str' in d:
                percent = d['_percent_str'].strip().replace('%', '')
                try:
                    percent = float(percent)
                    self.root.after(0, self.update_progress, percent)
                except ValueError:
                    pass
        elif d['status'] == 'finished':
            self.root.after(0, self.update_progress, 100)
            self.root.after(0, self.status_label.config, {"text": "Download finished, finalizing..."})

    def update_progress(self, percent):
        self.progress['value'] = percent
        self.status_label.config(text=f"Downloading: {percent:.2f}%")

    def reset_download_state(self):
        self.downloading = False
        self.root.after(0, self.download_button.config, {"state": tk.NORMAL})

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()