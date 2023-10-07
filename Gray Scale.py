from sys import exit
from subprocess import run, Popen
import cv2
import easygui
import numpy as np
from time import perf_counter
from os import remove
from os.path import basename, exists, expanduser, join, split
from sklearn.cluster import KMeans
from tkinter.messagebox import showinfo
from tqdm import tqdm
from pathlib import Path


def cartoonize_image(image, export=False, *args):
    img = None
    if type(image) == str:
        img = cv2.imread(image)
    else:
        img = image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert to grayscale and apply median blur to reduce image noise
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayimg = cv2.medianBlur(grayimg, 5)

    # Get the edges
    line_size = 3
    blur_value = 3
    edges = cv2.adaptiveThreshold(grayimg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)

    # Color quantization with KMeans clustering
    k = 7
    data = img.reshape(-1, 3)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto').fit(data)
    img_reduced = kmeans.cluster_centers_[kmeans.labels_]
    img_reduced = img_reduced.reshape(img.shape)
    img_reduced = img_reduced.astype(np.uint8)

    # Bilateral Filter
    blurred = cv2.bilateralFilter(img_reduced, d=7, sigmaColor=200, sigmaSpace=200)
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

    if export:
        path = None
        if args:
            if exists(args[0]):
                path = join(args[0], f'Cartoon-{basename(image)}')
            else:
                path = easygui.filesavebox(msg='Specified path doesn\'t exist. Save Cartoon Image to..',
                                           title='SAVE CARTOON IMAGE',
                                           default=join(expanduser("~"), 'Pictures', f'Cartoon-{basename(image)}'),
                                           filetypes=['.jpg', '.png', '.jpeg', '.bmp', '.webp'])

        else:
            path = easygui.filesavebox(msg='Save Cartoon Image to..',
                                       title='SAVE CARTOON IMAGE',
                                       default=join(expanduser("~"), 'Pictures', f'Cartoon-{basename(image)}'),
                                       filetypes=['.jpg', '.png', '.jpeg', '.bmp', '.webp'])

        # export cartoon to a jpg file
        cartoon_ = cv2.cvtColor(cartoon, cv2.COLOR_RGB2BGR)
        try:
            # print(f'Saving {path}')
            cv2.imwrite(path, cartoon_)
        except Exception as d:
            print(d)

    else:
        return cartoon


def cartoonize_video(video, export=False, out_fps=None, frame_width=None, frame_height=None, *args):
    if not exists(video):
        showinfo(title='Warning!', message=f"Video path not found.\n\t{video}")
        return

    video_path = video

    path = None
    if export:
        if args:
            if exists(args[0]):
                path = join(args[0], f'Cartoon-{basename(video_path)}')
            else:
                path = easygui.filesavebox(msg='Specified path doesn\'t exists. Save Cartoon Video to..',
                                           title='SAVE CARTOON VIDEO',
                                           default=join(expanduser("~"), 'Videos',
                                                        f'Cartoon-{basename(video_path)}'),
                                           filetypes=['.mp4', '.avi', '.mkv'])
        else:
            path = easygui.filesavebox(msg='Save Cartoon Video to..',
                                       title='SAVE CARTOON VIDEO',
                                       default=join(expanduser("~"), 'Videos', f'Cartoon-{basename(video_path)}'),
                                       filetypes=['.mp4', '.avi', '.mkv'])

    showinfo(title='Warning!',
             message='Video processing takes time. Do NOT close the application or all data will be lost.')

    video = cv2.VideoCapture(video)

    # Get the video properties
    if not frame_width:
        frame_width = int(video.get(3))
    if not frame_height:
        frame_height = int(video.get(4))
    fps = int(video.get(5))
    if not out_fps:
        out_fps = fps
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f'\tFile: {basename(video_path)}.\nFrame width: {int(video.get(3))}\t'
          f'Frame height: {int(video.get(4))}\tfps: {int(video.get(5))}\t'
          f'Total Frames: {frame_count}')

    output_path = join(expanduser('~'), 'temp-vid.mp4')

    # Define the codec and create a VideoWriter object to save the altered video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    for _ in tqdm(range(frame_count), desc='Creating Video: ', colour='green', unit='Frame'):
        ret, frame = video.read()
        # Break the loop when we reach the end of the video
        if not ret:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        grayscale_frame = cartoonize_image(frame)
        # Write the altered frame to the output video
        output_video.write(grayscale_frame)

    video.release()
    output_video.release()
    cv2.destroyAllWindows()

    if export:
        cmd = [
            'ffmpeg', '-nostdin', '-r', '16', '-i', f'{output_path}', '-i', f'{video_path}',
            f'{path}', '-y'
        ]
        run(cmd)

        try:
            remove(output_path)
        except Exception as e:
            print(e)

    else:
        return output_video


def cartoonize_folder_images(folder):
    if not exists(folder):
        return
    for child in tqdm(Path(folder).glob('*')):
        if child.is_file() and child.suffix in ['.jpg', '.png', '.jpeg', '.bmp', '.webp']:
            cartoonize_image(image=child, export=True, *folder)


if __name__ == '__main__':

    showinfo(title='Disclaimer!', message='\t\tWelcome\nChoose/Use high quality media for quality results.')

    prog_start = perf_counter()
    files = easygui.fileopenbox(msg='Open Image&/Video File(s) to cartoonize', title='OPEN IMAGE(s)&/VIDEO(s)',
                                default=join(expanduser("~"), 'Pictures', '*'),
                                filetypes=['.jpg', '.png', '.jpeg', '.bmp', '.webp', '.mp4', '.avi', '.mkv', 'Media '
                                                                                                             'Files'],
                                multiple=True)
    if files is None:
        showinfo(title='Exiting.', message='No file chosen..Press Enter to exit.')
        exit()

    for file in files:
        dir_name, name = split(file)
        ext = f'.{name.rsplit(".", maxsplit=1)[-1]}'
        # ext = base_name.rsplit(".", maxsplit=1)[-1]
        if ext in ['.jpg', '.png', '.jpeg', '.bmp', '.webp']:
            cartoonize_image(image=file, export=True)
        elif ext in ['.mp4', '.avi', '.mkv']:
            cartoonize_video(video=file, export=True, out_fps=16)
        else:
            showinfo(title='Warning!', message=f'File not a Media File/Unsupported:\n\t {file}\n')
            # print(f'File not a Media File/Unsupported:\n\t {file}\n')

    prog_end = perf_counter()
    showinfo(title='Execution Meter', message=f'Program took {prog_end - prog_start} seconds')

    Popen(['explorer', f'{join(expanduser("~"), "Pictures")}'], shell=True)
