import json
import subprocess
import os
import threading
import time

import tkinter as tk
from tkinterdnd2 import DND_TEXT, TkinterDnD

QBYIT_W_DIR = f"{os.path.expanduser('~')}\\.qbyit"

DOWNLOADS_PATH = f"{os.path.expanduser('~')}\\Downloads\\QbYit Downloads"
AUDIO_DOWNLOADS_PATH = f"{DOWNLOADS_PATH}\\Music"
VIDEO_DOWNLOADS_PATH = f"{DOWNLOADS_PATH}\\Videos"
DOCUMENT_DOWNLOADS_PATH = f"{DOWNLOADS_PATH}\\Documents"
IMAGE_DOWNLOADS_PATH = f"{DOWNLOADS_PATH}\\Pictures"
ARCHIVES_DOWNLOADS_PATH = f"{DOWNLOADS_PATH}\\Archives"
OTHER_DOWNLOADS_PATH = f"{DOWNLOADS_PATH}\\Others"

MAX_VID_HEIGHT = '720' # 720p Resolution.

def create_mutex():
    mutex_file = f"{QBYIT_W_DIR}\\RUN_ONCE"

    try:
        with open(mutex_file, 'a', encoding='utf-8', errors='ignore') as m:
            m.write("")
    except Exception as e:
        print(f" => Error creating a mutex...\n")
        log_progress(f"Error removing mutex...\n")

def remove_mutex():
    mutex_file = f"{QBYIT_W_DIR}\\RUN_ONCE"
    try:
        os.remove(mutex_file)
    except Exception as e:
        print(f"Error removing mutex...\n")
        log_progress(f"Error removing mutex...\n")

def log_progress(info):
    """Log mostly errors and exceptions."""
    
    log_file = f"{QBYIT_W_DIR}\\QbYit_LOG"
    current_time = time.asctime()

    try:
        with open(log_file, 'a', encoding='utf-8', errors='ignore') as t:
            t.write(f" =>[{current_time}]\n{info}\n\t--------------------------------------\n")
    except Exception as e:
        print(f" => Logging error.. Failed to create/read log file.\n{e}")

def check_paths():
    """Check to make sure download folders are available and set."""
    if not os.path.exists(DOWNLOADS_PATH):
        try:
            os.makedirs(DOWNLOADS_PATH, exist_ok=True)
        except Exception as e:
            log_progress(e)
            return

    paths_checklist = (QBYIT_W_DIR, 
                       AUDIO_DOWNLOADS_PATH, 
                       VIDEO_DOWNLOADS_PATH, 
                       DOCUMENT_DOWNLOADS_PATH, 
                       IMAGE_DOWNLOADS_PATH, 
                       ARCHIVES_DOWNLOADS_PATH, 
                       OTHER_DOWNLOADS_PATH)
    
    for path_item in paths_checklist:
        if not os.path.exists(path_item):
            try:
                os.makedirs(path_item)
            except Exception as e:
                log_progress(e)

    return

def check_ffmpeg():
    """Check if Ffmpeg is added to Windows Path or if its in the current working directory."""
    try:
        subprocess.run(['ffmpeg', '-version'], creationflags=subprocess.CREATE_NO_WINDOW)
        return True
    except FileNotFoundError:
        try:
            subprocess.run([f'{os.getcwd()}\\ffmpeg.exe', '-version'], creationflags=subprocess.CREATE_NO_WINDOW)
            return True
        except Exception as e:
            log_progress(e)
            return False

def check_yt_dlp():
    """Check if yt-dlp is added to Windows Path or if its in the current working directory."""
    try:
        subprocess.run(['yt-dlp', '--version'], creationflags=subprocess.CREATE_NO_WINDOW)
        return True
    except FileNotFoundError:
        try:
            subprocess.run([f'{os.getcwd()}\\yt-dlp.exe', '--version'], creationflags=subprocess.CREATE_NO_WINDOW)
            return True
        except Exception as e:
            log_progress(e)
            return False

def get_link_info(url: str):
    """Gets link info if available. Returns a dictionary."""
    info_command = f'yt-dlp -J {url}'
    result = subprocess.run([info_command], creationflags=subprocess.CREATE_NO_WINDOW)
    # Parse JSON output
    video_info = json.loads(result.stdout)
    
    info_dict = {}
    if video_info:
        info_dict = {
            'Title': f'{video_info.get("title")}',
            'Uploader': f'{video_info.get("uploader")}',
            'Duration': f'{video_info.get("duration")}'
        }
    
        # Print some information (you can modify this as needed)
    #print("Title:", video_info.get('title'))
    #print("Uploader:", video_info.get('uploader'))
    #print("Duration (seconds):", video_info.get('duration'))
    #print("View count:", video_info.get('view_count'))

    return info_dict

def download(urls: list, type, max_height = MAX_VID_HEIGHT):
    check_paths()   # Just to be safe

    url_str = ' '.join(urls).strip()
    # print(url_str)
    
    video_dl_command = [f'yt-dlp.exe', '-P', f'{VIDEO_DOWNLOADS_PATH}', '-f', f'bestvideo[height<={max_height}]+bestaudio/best[height<={max_height}]', '-o', '%(title)s.%(ext)s', f'{url_str}']
    audio_dl_command = [f'yt-dlp.exe', '-P', f'{AUDIO_DOWNLOADS_PATH}', '-x', '--audio-format', 'mp3', '-o', '%(title)s.%(ext)s', f'{url_str}']
    image_dl_command = [f'yt-dlp.exe', '-P', f'{IMAGE_DOWNLOADS_PATH}', '-o', '%(title)s.%(ext)s', f'{url_str}']
    doc_dl_command = [f'yt-dlp.exe', '-P', f'{DOCUMENT_DOWNLOADS_PATH}', '-o', '%(title)s.%(ext)s', f'{url_str}']
    archives_dl_command = [f'yt-dlp.exe', '-P', f'{ARCHIVES_DOWNLOADS_PATH}', '-o', '%(title)s.%(ext)s', f'{url_str}']
    others_dl_command = [f'yt-dlp.exe', '-P', f'{OTHER_DOWNLOADS_PATH}', '-o', '%(title)s.%(ext)s', f'{url_str}']

    def run(command: list):
        print(f"Command => {' '.join(command)}")
        try:
            ret_code = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return ret_code.returncode
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return 1
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return e.returncode

    match type:
        case "video":
            return run(video_dl_command)
        case "audio":
            return run(audio_dl_command)
        case "image":
            return run(image_dl_command)
        case "document":
            return run(doc_dl_command)
        case "archive":
            return run(archives_dl_command)
        case "other":
            return run(others_dl_command)
        case _:
            log_progress("Invalid type selected.")
            return 242

def create_panel():
    def drop(event):
        dropped_data = event.data.strip()
        print(f'Dropped link: {dropped_data}')
        
        def download_task():
            x = download([dropped_data], 'video', '480')
            if not x:
                print(f"\nDownload successful => {x}\n")
            else:
                print(f"\nDownload failed. => {x}\n")

        # Create and start a new thread for the download task
        download_thread = threading.Thread(target=download_task)
        download_thread.start()

    def pop_window(master):
        pass


    root = TkinterDnD.Tk()

    # Set the size of the window to be small, like an icon
    icon_size = 50
    root.geometry(f"{icon_size}x{icon_size}")

    # Position the window to the right middle of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = screen_width - icon_size - 10  # 10 pixels from the right edge
    y_position = (screen_height // 2) - (icon_size // 2)
    root.geometry(f"+{x_position}+{y_position}")

    # Ensure the window is always on top
    root.attributes('-topmost', True)

    # Remove the window decorations (title bar, etc.)
    root.overrideredirect(True)

    # Create a label as drop target
    label = tk.Label(root, text="Drop\nLink", bg="lightblue", relief='raised', width=icon_size, height=icon_size)
    label.pack(fill=tk.BOTH, expand=True)

    # Register the label as a drop target for text (URLs)
    label.drop_target_register(DND_TEXT)
    label.dnd_bind('<<Drop>>', drop)

    root.mainloop()

if __name__ == "__main__":
    create_mutex()
    check_paths()

    if not check_ffmpeg():
        log_progress("!!Sorry, can't continue. Ffmpeg not installed.\n"
              "....If ffmpeg is installed, try;\n"
              "=> Adding its bin directory to windows path in environment variables\n\t\tOR\n"
              "=> Placing its bin files in the same folder as this file.")
        print("Error starting app!")
        time.sleep(5)
        exit(1)

    if not check_yt_dlp():
        log_progress("!!Sorry, can't continue. Yt-dlp not installed.\n"
              "....If yt-dlp is installed, try;\n"
              "=> Placing its bin files in the same folder as this file.")
        print("Error starting app!")
        time.sleep(5)
        exit(1)

    create_panel()
    remove_mutex()
