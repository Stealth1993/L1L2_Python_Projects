import os
import re
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("700x400")  # Set fixed size
        self.root.resizable(False, False)  # Disable resizing
        self.root.configure(bg="#F0F0F0")  # Light gray background

        # Flag to track if a download is in progress
        self.downloading = False
        # Variable to track the current video index for playlists
        self.current_video_index = 0
        # Event to signal cancellation
        self.cancel_event = threading.Event()

        # URL Label and Entry
        self.url_label = tk.Label(root, text="YouTube URL:", bg="#F0F0F0", fg="#333333", font=("Helvetica", 12))
        self.url_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.url_entry = tk.Entry(root, width=40, bg="#FFFFFF", fg="#333333", font=("Helvetica", 10), relief="flat", borderwidth=2)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Type Dropdown
        self.type_label = tk.Label(root, text="Download Type:", bg="#F0F0F0", fg="#333333", font=("Helvetica", 12))
        self.type_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(root, textvariable=self.type_var, values=["Video with Audio", "Audio Only", "Video Only"], width=20, font=("Helvetica", 10))
        self.type_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.type_dropdown.bind("<<ComboboxSelected>>", self.update_quality_options)

        # Quality Dropdown
        self.quality_label = tk.Label(root, text="Quality:", bg="#F0F0F0", fg="#333333", font=("Helvetica", 12))
        self.quality_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.quality_var = tk.StringVar()
        self.quality_dropdown = ttk.Combobox(root, textvariable=self.quality_var, width=20, font=("Helvetica", 10))
        self.quality_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Destination Label and Entry
        self.dest_label = tk.Label(root, text="Download Destination:", bg="#F0F0F0", fg="#333333", font=("Helvetica", 12))
        self.dest_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.dest_entry = tk.Entry(root, width=30, bg="#FFFFFF", fg="#333333", font=("Helvetica", 10), relief="flat", borderwidth=2)
        self.dest_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.dest_entry.insert(0, self.get_default_download_path())
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_destination, bg="#BDBDBD", fg="#333333", font=("Helvetica", 10), relief="flat", width=10)
        self.browse_button.grid(row=3, column=2, padx=10, pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", style="green.Horizontal.TProgressbar")
        self.progress.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        # Status Label
        self.status_label = tk.Label(root, text="", bg="#F0F0F0", fg="#333333", font=("Helvetica", 10))
        self.status_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Download Button
        self.download_button = tk.Button(root, text="Download", command=self.start_download, bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 12), relief="flat", width=15)
        self.download_button.grid(row=6, column=0, padx=10, pady=20)

        # Cancel Button
        self.cancel_button = tk.Button(root, text="Cancel", command=self.cancel_download, state=tk.DISABLED, bg="#FFC107", fg="#333333", font=("Helvetica", 12), relief="flat", width=15)
        self.cancel_button.grid(row=6, column=1, padx=10, pady=20)

        # Exit Button
        self.exit_button = tk.Button(root, text="Exit", command=root.quit, bg="#F44336", fg="#FFFFFF", font=("Helvetica", 12), relief="flat", width=15)
        self.exit_button.grid(row=6, column=2, padx=10, pady=20)

        # Configure green progress bar style
        style = ttk.Style()
        style.theme_use('default')
        style.configure("green.Horizontal.TProgressbar", troughcolor='#E0E0E0', background='#4CAF50', bordercolor='#333333', lightcolor='#4CAF50', darkcolor='#4CAF50')

    def get_default_download_path(self):
        return os.path.join(os.path.expanduser("~"), "Downloads", "YouTubeDownloads")

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

    def clean_title(self, title):
        invalid_chars = r'[\/:*?"<>|]'
        cleaned = re.sub(invalid_chars, '', title)
        words = cleaned.split()[:3]
        folder_name = ' '.join(words) if words else "Download"
        return folder_name

    def start_download(self):
        if self.downloading:
            messagebox.showinfo("Info", "A download is already in progress. Please wait.")
            return

        self.downloading = True
        self.download_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.status_label.config(text="Preparing download...")

        self.download_thread = threading.Thread(target=self.download_video, daemon=True)
        self.download_thread.start()

    def cancel_download(self):
        if self.downloading:
            self.cancel_event.set()
            self.status_label.config(text="Cancelling download...")
            self.download_thread.join(timeout=5)
            self.reset_download_state()

    def download_video(self):
        url = self.url_entry.get()
        type_selected = self.type_var.get()
        quality_selected = self.quality_var.get()
        output_path = self.dest_entry.get()

        if not url or not type_selected or not quality_selected:
            self.root.after(0, lambda: messagebox.showerror("Input Error", "Please fill in all fields."))
            self.reset_download_state()
            return

        ydl_check = yt_dlp.YoutubeDL({'quiet': True})
        try:
            info = ydl_check.extract_info(url, download=False)
            if 'entries' in info:
                is_playlist = True
                folder_name = self.clean_title(info['title'])
                output_template = os.path.join(output_path, folder_name, 'part-%(playlist_index)s - %(title)s.%(ext)s')
            else:
                is_playlist = False
                folder_name = self.clean_title(info['title'])
                output_template = os.path.join(output_path, folder_name, '%(title)s.%(ext)s')
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to retrieve video info: {e}"))
            self.reset_download_state()
            return

        output_dir = os.path.join(output_path, folder_name)
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to create directory: {e}"))
            self.reset_download_state()
            return

        ydl_opts = {
            'outtmpl': output_template,
            'progress_hooks': [self.progress_hook],
            'quiet': False,
            'nopart': False,
            'retries': 10,
        }

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

        self.progress['value'] = 0
        self.status_label.config(text="Starting download...")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            if self.cancel_event.is_set():
                self.root.after(0, lambda: self.status_label.config(text="Download cancelled"))
            else:
                self.root.after(0, lambda: messagebox.showerror("Download Error", f"An error occurred: {e}"))
        finally:
            self.reset_download_state()

    def progress_hook(self, d):
        if self.cancel_event.is_set():
            return

        if d['status'] == 'downloading':
            if 'playlist_index' in d and 'playlist_count' in d:
                if d['playlist_index'] != self.current_video_index:
                    self.current_video_index = d['playlist_index']
                    self.root.after(0, lambda: self.progress.config(value=0))
                    self.root.after(0, lambda: self.status_label.config(text=f"Downloading video {d['playlist_index']} of {d['playlist_count']}"))
                if '_percent_str' in d:
                    percent = d['_percent_str'].strip().replace('%', '')
                    try:
                        percent = float(percent)
                        self.root.after(0, lambda: self.progress.config(value=percent))
                    except ValueError:
                        pass
            else:
                if '_percent_str' in d:
                    percent = d['_percent_str'].strip().replace('%', '')
                    try:
                        percent = float(percent)
                        self.root.after(0, lambda: self.progress.config(value=percent))
                    except ValueError:
                        pass
                self.root.after(0, lambda: self.status_label.config(text="Downloading..."))
        elif d['status'] == 'finished':
            if 'playlist_index' in d and 'playlist_count' in d:
                if d['playlist_index'] == d['playlist_count']:
                    self.root.after(0, lambda: self.status_label.config(text="Download completed successfully!"))
            else:
                self.root.after(0, lambda: self.status_label.config(text="Download completed successfully!"))

    def reset_download_state(self):
        self.downloading = False
        self.current_video_index = 0
        self.cancel_event.clear()
        self.root.after(0, lambda: self.download_button.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.cancel_button.config(state=tk.DISABLED))

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()