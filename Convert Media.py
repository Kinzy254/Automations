import easygui
import os
import sys
import subprocess
from time import sleep
from concurrent.futures import ThreadPoolExecutor, wait


video_extensions = [
    ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg",
    ".m4v", ".3gp", ".ogv", ".ts", ".m2ts", ".vob", ".divx", ".xvid", ".rm",
    ".rmvb", ".dat", ".asf", ".mts", ".m2t", ".m2ts", ".ts", ".mxf", ".h264",
    ".h265", ".hevc", ".avchd", ".f4v"
]
audio_extensions = [
    ".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a", ".wma", ".aiff", ".amr", ".opus",
    ".ape", ".mka", ".pcm", ".ac3", ".dts", ".ra", ".mid", ".midi", ".alac", ".ape",
    ".dsd", ".wv", ".tta", ".mpc"
]

def ffmpeg_check():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    
def convert_media_files(media_name: list, output_type="mp3", output_folder=""):
    for name in media_name:

        if not os.path.exists(name):
            print(f"\nPath does not exist!! \'{name}\'\n")
            continue

        name = os.path.abspath(name)
        output_ext = f".{output_type}" if not output_type.startswith(".") else output_type

        if output_folder == "":
            output_folder = f"{os.path.split(name)[0]}"

        basename_without_ext = os.path.splitext(os.path.basename(name))[0]
        input_ext = (os.path.splitext(os.path.basename(name)))[1]
        output_name = f"{output_folder}\\{basename_without_ext}-Qbyit Converter{output_ext}"

        if input_ext in video_extensions or input_ext in audio_extensions and output_ext in audio_extensions or output_ext in video_extensions:
            progress_check = False
            ret_code = 9

            def print_progress():
                global progress_check
                while not progress_check:
                    my_range = range(0, 4)
                    for _ in my_range:
                        print(f"\rPlease wait {'>' * _}", end='', flush=True)
                        sleep(0.5)

            def run_command(cmd):
                global progress_check
                global ret_code

                print(f"\nWorking on \"{os.path.basename(name)}\"")

                ret_code = subprocess.call(cmd,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL , creationflags=subprocess.CREATE_NO_WINDOW)
                progress_check = True #Remember to make it false after execution.

            cmd_command = ["ffmpeg", "-i", name, output_name, "-y"]

            with ThreadPoolExecutor(max_workers=2) as executor:
                prog_future = executor.submit(print_progress)
                run_future = executor.submit(run_command, cmd_command)

                wait([prog_future, run_future])

            print(f"\nFinished \"{os.path.basename(name)}\" - Exit code ({ret_code})\n")

        else:
            print(f"\nError: File type not supported!! \'{os.path.basename(name)}\'\n")


def main():
    print("\n       CONVERT MEDIA FORMATS WITH --QBYIT--\n".center(140, "."))
    
    input_1 = ""
    
    while input_1 == "1" or "2" or "0":
        input_1 = input("\nPress 1 to enter media path or a comma-separated list like [\'path1\', \'path2\']\n"
                        "Press 2 to choose file(s) with Windows Explorer\n"
                        "Press 0 to Exit!\n\n")

        match input_1:
            case "1":
                buffer_paths_to_images = (f"{input('\nEnter \"Media path(s)\" [Hint: Drag media file(s) from Windows Explorer]\n')}")

                paths_to_images_list = [_.strip('"') for _ in buffer_paths_to_images.split('"') if _.strip('"').strip()]

                input_2 = input(f"\nEnter Output type (Choose from below):\n  Audio{audio_extensions}\n  Video{video_extensions}\n\n")
                if not input_2:
                    input_2 = "mp3"
                
                convert_media_files(paths_to_images_list, input_2)
            
            case "2":
                path_to_images = (easygui.fileopenbox("Select Media(s)", "QBYIT--",f"{os.path.expanduser('~')}\\Videos\\*.*" , multiple=True))
                
                input_2 = input(f"\nEnter Output type (Choose from below):\n  Audio{audio_extensions}\n  Video{video_extensions}\n\n")
                if not input_2:
                    input_2 = "mp3"
                
                if path_to_images is not None:
                    convert_media_files(path_to_images, input_2)

            case "0":
                return

            case _:
                print(f"\nInvalid input!!")

if __name__ == "__main__":

    if len(sys.argv) > 1:
        buffer_arg_list = sys.argv[1:]
        arg_list = []

        for arg_name in buffer_arg_list:
            formatted_arg_name = [_.strip('"') for _ in arg_name.split('"') if _ is not None or _ != ' ']
            
            arg_list.extend(formatted_arg_name)
        
        for argument in arg_list:
            if os.path.exists(argument):
                convert_media_files([argument])

            elif argument == "Browse" or argument == "browse":
                buffer_list = easygui.fileopenbox("Select Media", "QBYIT--",f"{os.path.expanduser('~')}\\Videos\\*.*" , multiple=True)
                if buffer_list is not None:
                    convert_media_files(buffer_list)

            else:
                print("Input error!!")
                continue

    else:
        main()
        