import glob
import os.path
import subprocess

from os.path import isfile, join


def convert_video(input_files_path, output_files_path):
    command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        input_files_path,
        "-c",
        "copy",
        output_files_path
    ]
    process = subprocess.Popen(command)
    process.wait()


files_extension = '.webm'

path = r'C:\Users\golki\OneDrive\Desktop\test'
path_with_ext = os.path.join(path, '*.webm')

files = sorted(glob.glob(path_with_ext))
filenames = [f"file '{f}'\n" for f in files if isfile(join(path_with_ext, f))
             and f.endswith(files_extension)]
files_amount = len(filenames)

input_dir_name = "output"
input_dir_path = os.path.join(path, input_dir_name)
if not os.path.exists(input_dir_path):
    os.makedirs(input_dir_path)

print(f"Найден(о) {files_amount} файл(ов)")

if files_amount > 0:
    input_files_path = os.path.join(path, 'list.txt')
    # output_filename = f"{filenames[0].split('.')[0][6:-7:]}_output{files_extension}"

    output_files_path = os.path.join(input_dir_path, "output.webm")

    with open(input_files_path, 'w', encoding='utf-8') as f:
        f.writelines(filenames)

    print(input_files_path)
    print(output_files_path)

    convert_video(input_files_path, output_files_path)

print("Обработка завершена.")
