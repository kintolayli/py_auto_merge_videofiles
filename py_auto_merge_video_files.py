import glob
import os
import subprocess
import time
from configparser import ConfigParser
from os.path import isfile, join

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

script_dir = os.path.dirname(os.path.realpath(__file__))
input_dir_name = "to_merge_video"
input_dir_path = os.path.join(script_dir, input_dir_name)
config_filepath = os.path.join(script_dir, "config.ini")
config = ConfigParser()

if os.path.exists(config_filepath):
    config.read(config_filepath)
else:
    if not os.path.exists(input_dir_path):
        os.makedirs(input_dir_path)

    config["Settings"] = {"folder_to_watch": input_dir_path}
    with open(config_filepath, "w") as config_file:
        config.write(config_file)

os.startfile(input_dir_path)
folder_to_watch = config.get("Settings", "folder_to_watch")


def get_file_size(path: str) -> int:
    return os.path.getsize(path)


def allowed_video_formats(path):
    path_endswith = path.split(".")[-1]
    return path_endswith in ("mp4",)


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


class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_size = 0
        self.last_change_time = time.time()
        print(
            f"Скрипт запущен и находится в ожидании.\nДля объединения нескольких видеофайлов,"
            f" поместите файлы формата '.mp4' в директорию:\n\n"
            f"{folder_to_watch}\n\n"
        )
        self.files = []
        self.flag = True

    def on_created(self, event):
        if event.is_directory:
            return
        if allowed_video_formats(event.src_path):
            file_extension = '.mp4'

            while self.flag:
                try:
                    current_size = get_file_size(event.src_path)
                    if current_size == self.last_size:

                        path_with_ext = os.path.join(folder_to_watch,
                                                     f'*{file_extension}')

                        files = sorted(glob.glob(path_with_ext))
                        filenames = [f"file '{f}'\n" for f in files if
                                     isfile(join(path_with_ext, f))
                                     and f.endswith(file_extension)]
                        files_amount = len(filenames)

                        print(f"Найден(о) {files_amount} файл(ов)")

                        if files_amount > 0:
                            input_files_path = os.path.join(folder_to_watch,
                                                            'list.txt')
                            # output_filename = f"{files[0].split('.')[0].split('_compressed')[0]}{file_extension}"
                            output_filename = f"{files[0].split('.')[0].split('_compressed')[0]}_merged{file_extension}"
                            output_files_path = os.path.join(event.src_path,
                                                             output_filename)

                            with open(input_files_path, 'w',
                                      encoding='utf-8') as f:
                                f.writelines(filenames)

                            print(input_files_path)
                            print(output_files_path)

                            convert_video(input_files_path,
                                          output_files_path)

                            for file in files:
                                os.unlink(file)
                            os.unlink(input_files_path)

                        print("Обработка завершена.")
                        self.flag = False
                    else:
                        self.last_size = current_size
                        self.last_change_time = time.time()
                        time.sleep(1)
                except Exception as e:
                    print(e)
                    time.sleep(1)


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_to_watch, recursive=False)
    observer.start()

    try:
        while observer.is_alive():
            # Метод `observer.join(timeout=None)` - принимает `timeout` в
            # секундах, блокирующий операцию на указанное время.
            # Если `timeout` отсутствует, то операция будет блокироваться
            # до тех пор, пока поток не завершится.
            observer.join(1)
    finally:
        observer.stop()
        observer.join()
