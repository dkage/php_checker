import os
#
#
path = '/Users/danilo/Sites/localhost/wwwroot/educfinAdm/'
#
#
# def get_iterator_all_files_name(dir_path):
#     files_path = os.listdir(dir_path)
#     dirs_path = [x[0] for x in os.walk(path)]
#     return files_path, dirs_path
#
#
# def print_files(prefix_path, filenames_array):
#     for file in filenames_array:
#         if os.path.isdir(prefix_path+file):
#             continue
#         print(file)
#
#
# filenames, dirs = get_iterator_all_files_name(path)
#
# print_files(path, filenames)
#
#
# print('\n--------------------\n')
#
# for directory in dirs:
#     print(directory)
#     if '.git' in directory or directory == 'js' or directory == 'css':
#         continue
#     print(directory)
#


# for x in os.walk(path):
#     print(x)

#
# def getListOfFiles(dirName):
#     # create a list of file and sub directories
#     # names in the given directory
#     listOfFile = os.listdir(dirName)
#     allFiles = list()
#     # Iterate over all the entries
#     for entry in listOfFile:
#         # Create full path
#         fullPath = os.path.join(dirName, entry)
#         # If entry is a directory then get the list of files in this directory
#         if os.path.isdir(fullPath):
#             allFiles = allFiles + getListOfFiles(fullPath)
#         else:
#             allFiles.append(fullPath)
#
#     return allFiles

def php_syntax_test(php_file):
    # TODO get path
    """Checks php file for syntax errors using php -lint"""
    cli_command = 'php -l ' + path + php_file + ' >/dev/null 2>&1'
    lint = os.system(cli_command)
    return 'OK' if lint == 0 else 'SYNTAX ERROR'
    # output = relative_path + file + '   ' + ('OK' if lint == 0 else 'SYNTAX ERROR')

def get_iterator_all_files_name(dir_path):
    """Return array with all files in directory, and another array with all subdirs in directory"""
    files_in_dir = os.listdir(dir_path)
    files_in_dir.sort()

    # Remove unwanted filenames
    files_to_ignore = ['.git', '.gitignore', '.idea', '.gitlab-ci.yml']
    files_in_dir = list(filter(lambda x: x not in files_to_ignore, files_in_dir))

    subdirs_in_dir = []
    for name in files_in_dir:
        if os.path.isdir(path + name):
            subdirs_in_dir.append(name)
            files_in_dir.remove(name)

    return files_in_dir, subdirs_in_dir


dirs_path = [x[0] for x in os.walk(path)]
# paths_to_ignore = ['.git', '.gitignore', '.idea', '.gitlab-ci.yml']
# dirs_path = list(filter(lambda x: x not in paths_to_ignore, dirs_path))

for each_path in dirs_path:
    if '.git' in each_path or '.idea' in each_path:
        continue
    print(each_path)
    files, dirs = get_iterator_all_files_name(each_path)
    for each_file in files:
        extension = each_file.rsplit('.', 1)[-1]
        if extension == 'php':
            output = each_file, php_syntax_test(each_file)
            print(output)
            print(each_file)
    print('\n\n')
