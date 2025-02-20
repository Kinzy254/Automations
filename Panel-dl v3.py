import json
import os
import time
import tkinter as tk
import random
from threading import Thread
from tkinter import ttk
from tkinterdnd2 import DND_TEXT, TkinterDnD
from tqdm import tqdm
import yt_dlp

# Define directories
BASE_DIR = os.path.expanduser('~')
DOWNLOADS_PATH = os.path.join(BASE_DIR, "Downloads", "QbYit Downloads")
DIRS = {
    "Audio": os.path.join(DOWNLOADS_PATH, "Music"),
    "Video": os.path.join(DOWNLOADS_PATH, "Videos"),
    "Documents": os.path.join(DOWNLOADS_PATH, "Documents"),
    "Images": os.path.join(DOWNLOADS_PATH, "Pictures"),
    "Archives": os.path.join(DOWNLOADS_PATH, "Archives"),
    "Other": os.path.join(DOWNLOADS_PATH, "Others"),
}
LOG_FILE = os.path.join(BASE_DIR, ".qbyit", "QbYit_LOG")

def log_progress(info):
    """Log errors and exceptions."""
    try:
        with open(LOG_FILE, 'a', encoding='utf-8', errors='ignore') as log:
            log.write(f"[{time.asctime()}] {info}\n")
    except Exception as e:
        print(f"Logging error: {e}")

def ensure_directories():
    """Ensure all necessary directories exist."""
    for path in DIRS.values():
        os.makedirs(path, exist_ok=True)


def get_link_info(link):
    """
    Get video metadata using yt_dlp as a Python module.
    Returns a dictionary with Title, Duration, Thumbnail, Uploader, ID, Subtitles, Playlist, and Formats.
    """
    try:
        ydl_opts = {
            "quiet": True,  # Suppress output for performance
            "no_warnings": True,
            "noplaylist": True,  # Prevents fetching entire playlists
            "skip_download": True,  # Do not download
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)

        if not info:
            return None

        # Extract relevant information
        link_info = {
            "Title": info.get("title"),
            "Duration": info.get("duration_string"),
            "Thumbnail": info.get("thumbnail"),
            "Uploader": info.get("uploader"),
            "ID": info.get("id"),
            "Subtitles": info.get("subtitles"),
            "Playlist": info.get("playlist"),
            "Formats": {
                fmt["format_id"]: {
                    "Format_ID": fmt.get("format_id"),
                    "Extension": fmt.get("ext"),
                    "Format_note": fmt.get("format_note"),
                    "Width": fmt.get("width"),
                    "Height": fmt.get("height"),
                    "Filesize": fmt.get("filesize"),
                }
                for fmt in (info.get("formats") or [])
                if (fmt.get("vcodec") and fmt.get("vcodec") != "none") or (fmt.get("acodec") and fmt.get("acodec") != "none")
            },
        }

        return link_info

    except Exception as e:
        print(f"Error fetching link info: {e}")
        return None

    '''
    FORMAT GENERAL RULE OF THUMB:
    > General options comes first
    > Format selection (-f) comes next
    > Output template (-o) before URL
    > Post processing options
    > URL always last.
    '''
def postprocess_callback(d): 
    """Handle postprocessing progress updates."""
    
    status = d.get('status')
    postprocessor = d.get('postprocessor', 'Unknown')

    if status == 'started':
        print(f"Started: {postprocessor}", end="\r")

    elif status == 'processing':
        # If progress tracking is available
        if 'progress' in d and 'max_progress' in d:
            print(f"{postprocessor} Progress: {d['progress'] / d['max_progress']}", end="\r")

        # If a message is available
        elif 'message' in d:
            print(f"{postprocessor}: {d['message']}", end="\r")

        else:
            print(f"{postprocessor} is processing...", end="\r")

    elif status == 'finished':
        print(f"Finished: {postprocessor}", end="\r")

    elif status == 'error':
        error_msg = d.get('error', 'Unknown error')
        print(f"Error in {postprocessor}: {error_msg}", end="\r")


def progress_callback(d):
    """Update progress bar using tqdm."""
    if d["status"] == "downloading":
        filename = os.path.basename(d["filename"])
        percent = d["_percent_str"].strip()
        downloaded = d["_downloaded_bytes_str"].strip()
        total_size = d["_total_bytes_str"].strip() if d["_total_bytes_str"] else "Unknown"
        speed = d["_speed_str"].strip() if d["_speed_str"] else "N/A"
        
        tqdm.write(f"{downloaded}/{total_size} | {percent} | {speed} || {filename}", end="\r")

    elif d["status"] == "finished":
        tqdm.write("\n")

def download(link, media_type="video", max_height="1080", audio_type="mp3"):
    """Download a video or audio file using yt-dlp as a module."""
    output_dir = DIRS.get(media_type.capitalize(), DIRS["Other"])
    
    print("Fetching video information...", end="\r")
    info_json = get_link_info(link)

    if not info_json:
        print("Failed to fetch video information.", end="\r")
        return

    video_ext = "mkv"  # Default extension

    ydl_opts = {
        "quiet": True,  # Suppress output
        "no_warnings": True,
        "noprogress": True,  # Disable progress bar
        "windows-filename": True,  # Ensure compatibility with Windows
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "no_mtime": True,
        "noplaylist": True,
        "progress_hooks": [progress_callback],  # Hook for progress updates
        "postprocessor_hooks": [postprocess_callback],  # Hook for postprocessing updates
    }

    if media_type == "video":
        ydl_opts["format"] = f"bestvideo[height<={max_height}]+bestaudio/best[height<={max_height}]/best"
        ydl_opts["merge_output_format"] = video_ext  # Ensure desired video output
        ydl_opts["embedsubtitles"] = True
        ydl_opts["embedthumbnail"] = True
        ydl_opts["postprocessors"] = [
            {"key": "FFmpegMetadata"},
        ]
    elif media_type == "audio":
        ydl_opts["format"] = "bestaudio"
        ydl_opts["embedthumbnail"] = True
        ydl_opts["postprocessors"] = [
            {"key": "FFmpegExtractAudio", "preferredcodec": audio_type},
            {"key": "FFmpegMetadata"},
        ]

    print(f"Starting download: {info_json['Title']}")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        print(f"\nDownload complete. ({info_json['Title']})\n")

    except Exception as e:
        print(f"Download error: {e}")


def create_panel():
    """Create a drag-and-drop panel with audio/video download options."""
    def drop(event):
        link = event.data.strip()
        expand_window(link)

    def expand_window(link):
        root.geometry("200x100")
        label.pack_forget()
        root.geometry(f"+{x - 150}+{y}")  # Expand leftwards

        def reset_panel():
            for widget in btn_audio_frame.winfo_children() + btn_video_frame.winfo_children():
                widget.destroy()
            btn_audio_frame.pack_forget()
            btn_video_frame.pack_forget()
            root.geometry("50x50")
            root.geometry(f"+{x}+{y}")
            label.pack(fill=tk.BOTH, expand=True)

        def start_download(media_type, value):
            Thread(target=download, args=(link, media_type, value), daemon=True).start()
            reset_panel()

        btn_audio_frame = tk.Frame(root)
        btn_audio_frame.pack(fill=tk.BOTH, expand=True)
        
        audio_types = ["mp3", "m4a", "flac", "wav"]
        selected_atype = tk.StringVar(value="mp3")
        ttk.Button(btn_audio_frame, text="Audio", command=lambda: start_download("audio", selected_atype.get())).pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        ttk.OptionMenu(btn_audio_frame, selected_atype, *audio_types).pack(fill=tk.BOTH, side=tk.RIGHT)
        
        btn_video_frame = tk.Frame(root)
        btn_video_frame.pack(fill=tk.BOTH, expand=True)

        resolutions = ["720", "480", "1080", "2160"]
        selected_res = tk.StringVar(value="2160")
        ttk.Button(btn_video_frame, text="Video", command=lambda: start_download("video", selected_res.get())).pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        ttk.OptionMenu(btn_video_frame, selected_res, *resolutions).pack(fill=tk.BOTH, side=tk.RIGHT)
    
    root = TkinterDnD.Tk()
    root.geometry("50x50")
    root.attributes('-topmost', True)
    root.overrideredirect(True)
    
    x, y = root.winfo_screenwidth() - 60, random.randint(0, root.winfo_screenheight() - 50)
    root.geometry(f"+{x}+{y}")

    label = tk.Label(root, text="Drop\nLink", bg="lightblue", relief='raised')
    label.pack(fill=tk.BOTH, expand=True)
    label.drop_target_register(DND_TEXT)
    label.dnd_bind('<<Drop>>', drop)

    root.mainloop()

# Ensure directories exist before running
ensure_directories()
create_panel()
