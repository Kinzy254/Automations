from easygui import fileopenbox
from os import path, remove
import sys
from subprocess import run, CalledProcessError, PIPE, DEVNULL, CREATE_NO_WINDOW
from time import perf_counter, sleep

ffmpeg_path = "ffmpeg"

video_extensions = (
    ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg",
    ".m4v", ".3gp", ".ogv", ".ts", ".m2ts", ".vob", ".divx", ".xvid", ".rm",
    ".rmvb", ".dat", ".asf", ".mts", ".m2t", ".m2ts", ".ts", ".mxf", ".h264",
    ".h265", ".hevc", ".avchd", ".f4v"
)
audio_extensions = (
    ".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a", ".wma", ".aiff", ".amr", ".opus",
    ".ape", ".mka", ".pcm", ".ac3", ".dts", ".ra", ".mid", ".midi", ".alac", ".ape",
    ".dsd", ".wv", ".tta", ".mpc"
)

video_resolutions = {
    '144p': '256x144',
    '240p': '426x240',
    '360p': '640x360',
    '480p': '854x480',
    '720p': '1280x720',
    '1080p': '1920x1080',
    '1440p': '2560x1440',
    '2160p': '3840x2160',
    '4320p': '7680x4320'
}

def ffmpeg_check():
    try:
        run([ffmpeg_path, "-version"], stdout=PIPE, stderr=PIPE, check=True)
        return True
    except CalledProcessError:
        return False
    
def convert_media_files(media_name: list, output_type="mp3", resolution='1280x720', output_folder="", delete_status=False):
    total_files = len(media_name)
    count = 1

    for name in media_name:

        if not path.exists(name):
            print(f"\nPath does not exist!! \'{name}\'\n")
            continue

        name = path.abspath(name)
        output_ext = f".{output_type}" if not output_type.startswith(".") else output_type

        if output_folder == "":
            output_folder = f"{path.split(name)[0]}"

        basename_without_ext = path.splitext(path.basename(name))[0]
        input_ext = (path.splitext(path.basename(name)))[1]
        output_name = f"{output_folder}\\{basename_without_ext}-Qbyit Converter{output_ext}"

        if "-Qbyit Converter" in f"{basename_without_ext}{output_ext}":
            print(f"Converted file exists!! => {path.basename(name)}")
            prompt_1 = input(" ..Delete existing file?\n\t1> Yes\n\t2> No\n")
            if prompt_1 not in ("1", "Yes", "yes", "Y", "y", "True", "true"):
                print("Okay, Exiting...")
                sleep(3)
                continue
            else:
                delete_status = True

        if input_ext in video_extensions or input_ext in audio_extensions and output_ext in audio_extensions or output_ext in video_extensions:

#            def print_progress():
#                global progress_check
#                while not progress_check:
#                    my_range = range(0, 4)
#                    for _ in my_range:
#                        print(f"\rPlease wait {'>' * _}", end='', flush=True)
#                        sleep(0.5)

            cmd_command = [ffmpeg_path, "-i", name, "-vf", f"scale={resolution}", output_name, "-y"]

            print(f"\n..{count}/{total_files}\nConverting \"{path.basename(name)}\"")

            ret_code = run(cmd_command, stdout=PIPE, stderr=DEVNULL, creationflags=CREATE_NO_WINDOW)

            print(f"....Done - Exit code ({ret_code.returncode})")
            count += 1

            if delete_status:
                try:
                    remove(name)
                    print("Original file removed.\n")
                except Exception as e:
                    print(f"Error removing original.\n\t{e}\n")


        else:
            print(f"\nError: File type not supported!! \'{path.basename(name)}\'\n")


def main():
    print("\n       --QBYIT-- AUDIO/VIDEO CONVERTER\n".center(140, "."))
    
    input_1 = ""
    
    while input_1 == "1" or "2" or "3" or "0":
        input_1 = input("\n\t***OPTIONS***\n"
                        "1: Enter media path or a comma-separated list like [\'path1\', \'path2\']\n"
                        "2: Choose file(s) with Windows Explorer\n"
                        "3: Accumulate files\n"
                        "0: Exit!\n\n")

        match input_1:
            case "1":
                buffer_paths_to_files = (f"{input('\nEnter \"Media path(s)\" [Hint: Drag media file(s) from Windows Explorer]\n')}")

                paths_to_files_list = [_.strip('"') for _ in buffer_paths_to_files.split('"') if _.strip('"').strip()]

                input_2 = input(f"\nEnter Output type (Choose from below):\n  Audio{audio_extensions}\n  Video{video_extensions}\n\n")
                if not input_2:
                    input_2 = "mp3"

                res = ""
                if f".{input_2}" in video_extensions or input_2 in video_extensions:
                    res = input(f"\n => Choose video resolution...\n{tuple(video_resolutions.keys())}\n\n")
                    if res is None or res not in video_resolutions:
                        res = "1280x720"
                        raise ValueError("\n    Unsupported Resolution! Going for default(720p).\n")
                    

                del_status: bool
                buf_del_status = input("\nDelete original files? (Yes/No) [Default - 'No']")

                true_its = ("Yes", "yes", "Y", "y", "True", "true")
                false_its = ("No", "no", "N", "n", "False", "false")

                if buf_del_status in true_its:
                    del_status = True
                elif buf_del_status in false_its:
                    del_status = False
                else:
                    print(f"  => Delete_status defaulting to False.\n")
                    del_status = False
                print(f"\nTotal files => {len(paths_to_files_list)}\n")

                start_time = perf_counter()
                convert_media_files(paths_to_files_list, input_2, delete_status=del_status, resolution=f"{video_resolutions.get(res)}")
                end_time = perf_counter()

                print(f"....Time taken => {int(end_time-start_time)} s => {len(paths_to_files_list)} file(s)\n")
            
            case "2":
                path_to_files = (fileopenbox("Select Media(s)", "QBYIT--",f"{path.expanduser('~')}\\Videos\\*.*" , multiple=True))
                
                input_2 = input(f"\nEnter Output type (Choose from below):\n  Audio{audio_extensions}\n  Video{video_extensions}\n\n")
                if not input_2:
                    input_2 = "mp3"

                res = ""
                if f".{input_2}" in video_extensions or input_2 in video_extensions:
                    res = input(f"\n => Choose video resolution...\n{tuple(video_resolutions.keys())}\n\n")
                    if res is None or res not in video_resolutions:
                        res = "1280x720"
                        raise ValueError("  Unsupported Resolution! Going for default(720p).\n")
                    
                del_status: bool
                buf_del_status = input("\nDelete original files? (Yes/No) [Default - 'No']")
                
                true_its = ("Yes", "yes", "Y", "y", "True", "true")
                false_its = ("No", "no", "N", "n", "False", "false")

                if buf_del_status in true_its:
                    del_status = True
                elif buf_del_status in false_its or buf_del_status == None:
                    del_status = False
                else:
                    print(f"\n  => Delete_status defaulting to False.\n")
                    del_status = False
                
                if path_to_files is not None:
                    print(f"\nTotal files => {len(path_to_files)}\n")

                    start_time = perf_counter()
                    convert_media_files(path_to_files, input_2, delete_status=del_status, resolution=f"{video_resolutions.get(res)}")
                    end_time = perf_counter()

                    print(f"\n....Time taken => {int(end_time-start_time)} s\n")

            case "3":
                full_list = []
                input_z = ""

                while input_z == "1" or "2" or "0":
                    print(f"Full list has => {len(full_list)} file(s)\n")
                    input_z = input("\t***Accumulator Options***\n"
                                    "  =>1: Enter media path/a comma-separated list like [\'path1\', \'path2\']\n"
                                    "  =>2: Choose with Windows Explorer\n"
                                    "  =>0: Enough!\n\n")
                    
                    match input_z:
                        case "1":
                            buffer_paths_to_files = (f"{input('\nEnter \"Media path(s)\" [Hint: Drag media file(s) from Windows Explorer]\n')}")

                            paths_to_files_list = [_.strip('"') for _ in buffer_paths_to_files.split('"') if _.strip('"').strip()]
                            if paths_to_files_list is not None:
                                full_list.extend(paths_to_files_list)

                        case "2":
                            path_to_files = (fileopenbox("Select Media(s)", "QBYIT--",f"{path.expanduser('~')}\\Videos\\*.*" , multiple=True))
                            if path_to_files is not None:
                                full_list.extend(path_to_files)

                        case "0":
                            break

                        case _:
                            print("\n   Invalid input!!")

                if len(full_list) == 0:
                    print("!!No files added to list.\n")
                    continue

                input_2 = input(f"\nEnter Output type (Choose from below):\n  Audio{audio_extensions}\n  Video{video_extensions}\n\n")
                if not input_2:
                    input_2 = "mp3"

                res = ""
                if f".{input_2}" in video_extensions or input_2 in video_extensions:
                    res = input(f"\n => Choose video resolution...\n{tuple(video_resolutions.keys())}\n\n")
                    if res is None or res not in video_resolutions:
                        res = "1280x720"
                        raise ValueError("Unsupported Resolution! Going for default(720p).\n")

                del_status: bool
                buf_del_status = input("\nDelete original files? (Yes/No) [Default - 'No']")
                
                true_its = ("Yes", "yes", "Y", "y", "True", "true")
                false_its = ("No", "no", "N", "n", "False", "false")

                if buf_del_status in true_its:
                    del_status = True
                elif buf_del_status in false_its or buf_del_status == None:
                    del_status = False
                else:
                    print(f"\n  => Delete_status defaulting to False.\n")
                    del_status = False
                
                if full_list is not None:
                    print(f"Total files => {len(full_list)}\n")

                    start_time = perf_counter()
                    convert_media_files(full_list, input_2, delete_status=del_status, resolution=f"{video_resolutions.get(res)}")
                    end_time = perf_counter()

                    print(f"\n....Time taken => {int(end_time-start_time)} s\n")

            case "0":
                return

            case _:
                print(f"\nInvalid input!!")

if __name__ == "__main__":

    if not ffmpeg_check():
        print("!!Sorry, can't continue. Ffmpeg not installed.\n"
              "....If ffmpeg is installed, try;\n"
              "=> Adding its bin directory to windows path in environment variables\n\t\tOR\n"
              "=> Placing its bin files in the same folder as this file.")
        sleep(5)
        exit(1)

    if len(sys.argv) > 1:
        buffer_arg_list = sys.argv[1:]
        arg_list = []

        for arg_name in buffer_arg_list:
            formatted_arg_name = [_.strip('"') for _ in arg_name.split('"') if _ is not None or _ != ' ']
            
            arg_list.extend(formatted_arg_name)
        
        for argument in arg_list:
            if path.exists(argument):
                convert_media_files([argument])

            elif argument == "Browse" or argument == "browse":
                buffer_list = fileopenbox("Select Media", "QBYIT--",f"{path.expanduser('~')}\\Videos\\*.*" , multiple=True)
                if buffer_list is not None:
                    convert_media_files(buffer_list)

            else:
                print("Input error!!")
                continue

    else:
        try:
            main()

        except Exception as e:
            print(f'\n{e}\n')
    input("\n >>>Nice to see you..BYE.")
        