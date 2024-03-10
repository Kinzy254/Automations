import rembg
import os
import sys
import re
import cv2
import easygui

def remove_background(images_list: list, output_folder="", model_name="isnet-general-use"):
    model_path_folder = f"{os.path.expanduser('~')}\\.u2net"

    if not os.path.exists(model_path_folder):
        match input("\nDownload model? Y/N\n"):
            case "N":
                return
            case "n":
                return
        
    rembg_session = rembg.new_session(model_name)

    for image in images_list:
        if output_folder == "":
            output_folder = f"{os.path.split(image)[0]}"

        if not os.path.exists(image):
            print(f"\nPath does not exist! \'{image}\'\n")
            continue

        image = os.path.abspath(image)
        base_name = os.path.splitext(os.path.basename(image))[0]
        output_name = f"{output_folder}\\{base_name}-RemBG.png"

        print(f"\nWorking on \'{os.path.basename(image)}\'")

        input = cv2.imread(image)
        if input is not None and not os.path.exists(output_name):
            output = rembg.remove(input, session=rembg_session)
            cv2.imwrite(output_name, output)

            print(f"Done..... 100%\n")

        else:
            print(f"Skipping \'{os.path.basename(image)}\'. Error while working or file exists\n")


def main():
    print("\n       REMOVE IMAGE BACKGROUND WITH --QBYIT--\n".center(140, "."))
    
    input_1 = ""
    
    while input_1 == "1" or "2" or "0":
        input_1 = input("\nPress 1 to enter image path or a comma-separated list like [\'path1\', \'path2\']\n"
                        "Press 2 to choose file(s) with Windows Explorer\n"
                        "Press 0 to Exit!\n\n")
        match input_1:
            case "1":
                buffer_paths_to_images = (f"{input('\nEnter \"image path(s)\" [Hint: Drag image file(s) from Windows Explorer]\n')}")

                paths_to_images_list = [_.strip('"') for _ in buffer_paths_to_images.split('"') if _.strip('"').strip()]

                remove_background(paths_to_images_list)
            
            case "2":
                path_to_images = (easygui.fileopenbox("Select Image(s)", "QBYIT--",f"{os.path.expanduser('~')}\\Pictures\\*.*" , multiple=True))
                if path_to_images is not None:
                    remove_background(path_to_images)

            case "0":
                return

            case _:
                print(f"\nInvalid input!!")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        buffer_arg_list = sys.argv[1:]
        arg_list = []

        for arg_name in buffer_arg_list:
            formatted_arg_name = [_.strip('"') for _ in arg_name.split('"') if _ is not None or _ != ' ']
            
            arg_list.extend(formatted_arg_name)
        
        for argument in arg_list:
            if os.path.exists(argument):
                remove_background([argument])

            elif argument == "Browse" or argument == "browse":
                buffer_list = easygui.fileopenbox("Select Image(s)", "QBYIT--",f"{os.path.expanduser('~')}\\Pictures\\*.*" , multiple=True)
                if buffer_list is not None:
                    remove_background(buffer_list)

            else:
                print("Input error!!")
                continue

    else:
        main()
