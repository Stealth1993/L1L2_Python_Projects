import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("400x300")  # Adjusted height after removing labels
        self.root.resizable(False, False)
        self.root.configure(bg="#F0F0F0")

        # Cancellation event
        self.cancel_event = threading.Event()

        # URL Entry
        tk.Label(root, text="YouTube URL:", bg="#F0F0F0", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10)
        self.url_entry = tk.Entry(root, width=40)
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

        # Type Selection
        tk.Label(root, text="Download Type:", bg="#F0F0F0", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10)
        self.type_var = tk.StringVar(value="video")
        tk.Radiobutton(root, text="Video", variable=self.type_var, value="video", bg="#F0F0F0").grid(row=1, column=1)
        tk.Radiobutton(root, text="Audio", variable=self.type_var, value="audio", bg="#F0F0F0").grid(row=1, column=2)

        # Quality Selection
        tk.Label(root, text="Quality:", bg="#F0F0F0", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10)
        self.quality_var = tk.StringVar(value="best")
        qualities = ["best", "medium", "low"]
        self.quality_menu = ttk.Combobox(root, textvariable=self.quality_var, values=qualities, state="readonly")
        self.quality_menu.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

        # Progress Label
        self.progress_label = tk.Label(root, text="Progress: 0%", bg="#F0F0F0", fg="#333333", font=("Helvetica", 10))
        self.progress_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        # Status Label
        self.status_label = tk.Label(root, text="Ready", bg="#F0F0F0", fg="#333333", font=("Helvetica", 10))
        self.status_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

        # Buttons
        self.download_button = ttk.Button(root, text="Download", command=self.start_download)
        self.download_button.grid(row=5, column=0, pady=10)

        self.cancel_button = ttk.Button(root, text="Cancel", command=self.cancel_download, state="disabled")
        self.cancel_button.grid(row=5, column=1, pady=10)

        self.exit_button = ttk.Button(root, text="Exit", command=root.quit)
        self.exit_button.grid(row=5, column=2, pady=10)

        self.current_playlist_index = None
        self.download_thread = None

    def progress_hook(self, d):
        if self.cancel_event.is_set():
            raise Exception("Download cancelled")
        if d['status'] == 'downloading':
            try:
                percent_str = d.get('_percent_str', '0%')
                percent = float(percent_str.replace('%', ''))

                # Update progress label
                self.root.after(0, lambda: self.progress_label.config(text=f"Progress: {percent:.2f}%"))

                # Handle playlist progress
                playlist_index = d.get('playlist_index', 1)
                playlist_count = d.get('playlist_count', 1)
                if playlist_count > 1:
                    status_text = f"Downloading video {playlist_index} of {playlist_count}: {percent:.2f}%"
                else:
                    status_text = f"Downloading: {percent:.2f}%"
                self.root.after(0, lambda: self.status_label.config(text=status_text))
                
            except (ValueError, KeyError):
                self.root.after(0, lambda: self.status_label.config(text="Downloading. Please wait..."))
        elif d['status'] == 'finished':
            self.root.after(0, lambda: self.progress_label.config(text="Progress: 100%"))
            self.root.after(0, lambda: self.status_label.config(text="Download completed"))

    def download_video(self, url, download_type, quality):
        try:
            # Set download path
            download_path = os.path.join(os.path.expanduser("~"), "Downloads", "YouTubeDownloads")
            if not os.path.exists(download_path):
                os.makedirs(download_path)

            # Get video/playlist title
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                if 'entries' in info:
                    title = info['entries'][0].get('title', 'playlist')

            # Create subdirectory with first three words of title
            first_three_words = ' '.join(title.split()[:3])
            subdir = os.path.join(download_path, first_three_words)
            if not os.path.exists(subdir):
                os.makedirs(subdir)

            ydl_opts = {
                'progress_hooks': [self.progress_hook],
                'outtmpl': os.path.join(subdir, '%(title)s.%(ext)s'),
            }

            if download_type == "video":
                ydl_opts['format'] = 'bestvideo+bestaudio/best' if quality == "best" else 'worst'
            else:  # audio
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192' if quality == "best" else '96',
                }]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.root.after(0, lambda: self.status_label.config(text="Connecting to YouTube..."))
                ydl.download([url])
        except Exception as e:
            if str(e) == "Download cancelled":
                self.root.after(0, lambda: self.status_label.config(text="Download cancelled"))
            else:
                self.root.after(0, lambda: self.status_label.config(text=f"Error: {str(e)}"))
                messagebox.showerror("Error", f"Download failed: {str(e)}")

    def start_download(self):
        if self.download_thread and self.download_thread.is_alive():
            messagebox.showwarning("Warning", "A download is already in progress.")
            return

        url = self.url_entry.get().strip()
        download_type = self.type_var.get()
        quality = self.quality_var.get()

        if not url:
            messagebox.showwarning("Input Error", "Please enter a YouTube URL")
            return

        self.progress_label.config(text="Progress: 0%")
        self.status_label.config(text="Starting download...")
        self.download_button.config(state="disabled")
        self.cancel_button.config(state="normal")

        self.cancel_event.clear()
        self.download_thread = threading.Thread(target=self.download_video, args=(url, download_type, quality), daemon=True)
        self.download_thread.start()

        def check_thread():
            if self.download_thread.is_alive():
                self.root.after(100, check_thread)
            else:
                self.download_button.config(state="normal")
                self.cancel_button.config(state="disabled")
        self.root.after(100, check_thread)

    def cancel_download(self):
        if self.download_thread and self.download_thread.is_alive():
            self.cancel_event.set()
            self.status_label.config(text="Cancelling download...")
            self.download_thread.join()
            self.download_button.config(state="normal")
            self.cancel_button.config(state="disabled")
            self.status_label.config(text="Download cancelled")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()