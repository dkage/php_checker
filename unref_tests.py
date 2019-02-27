import os


path = '/Users/danilo/Sites/localhost/wwwroot/educfinAdm/'


def get_iterator_all_files_name(dir_path):
    files_path = os.listdir(dir_path)
    dirs_path = [x[0] for x in os.walk(path)]
    return files_path, dirs_path


def print_files(prefix_path, filenames_array):
    for file in filenames_array:
        if os.path.isdir(prefix_path+file):
            continue
        print(file)


filenames, dirs = get_iterator_all_files_name(path)

print_files(path, filenames)


print('\n--------------------\n')

for directory in dirs:
    print(directory)
    if '.git' in directory or directory == 'js' or directory == 'css':
        continue
    print(directory)

