import os.path
from os import listdir
from os.path import isfile, join

print(
    "Введите путь до папки, где находятся файлы, которые необходимо "
    "объединить:\n")
while True:
    path = input()
    if len(path) > 0:
        break
    print("Вы ничего не ввели, попробуйте еще раз.")

extensions_dict = {
    '1': '.webm',
    '2': '.mp4'
}
print("Введите расширение файла(ов), которые будут объединяться (1 - '.webm', "
      "2 - '.mp4', либо введите вручную в формате '.<расширение>':\n")
ext_input = input()
files_extension = extensions_dict.get(ext_input)
if not files_extension:
    files_extension = ext_input

filenames = [f"file '{f}'\n" for f in listdir(path) if isfile(join(path, f))
             and f.endswith(files_extension)]
files_amount = len(filenames)

print(f"Найден(о) {files_amount} файл(ов)")

if files_amount > 0:
    input_files_path = os.path.join(path, 'list.txt')
    output_filename = f"{filenames[0].split('.')[0][6:-7:]}_output{files_extension}"
    output_files_path = os.path.join(path, output_filename)

    with open(input_files_path, 'w', encoding='utf-8') as f:
        f.writelines(filenames)

    print(input_files_path)
    print(output_files_path)

    command = f'ffmpeg -safe 0 -f concat -i "{input_files_path}" -c copy "{output_files_path}"'
    print(command)

    os.system(command)

print("Обработка завершена.")
