import io
import os
import re
import sys
from termcolor import colored


def get_iterator_all_files_name(dir_path):
    """Return array with all files in directory, and another array with all subdirs in directory"""
    files_in_dir = os.listdir(dir_path)
    files_in_dir.sort()

    # Remove unwanted filenames and subdirectories
    ignore = ['.git', '.gitignore', '.idea', '.gitlab-ci.yml']
    files_in_dir = list(filter(lambda f: not(f in ignore) and not os.path.isdir(dir_path + f), files_in_dir))

    # print(files_in_dir)
    return files_in_dir


def php_syntax_test(php_path, php_file):
    """Checks php file for syntax errors using php -lint"""
    cli_command = 'php -l ' + php_path + php_file + ' >/dev/null 2>&1'
    lint = os.system(cli_command)
    return lint != 0


# Check if has a
if len(sys.argv) == 1:
    print('Insira o caminho absoluto do diretório a ser analisado')
    sys.exit()

# Analyzed project root folder - absolute path
path = sys.argv[1]

# Checks if the directory exists
if not os.path.isdir(path):
    print('Diretório não encontrado')
    sys.exit()

print('Analisando arquivos...')


# Creates array with every directory and subdirs and remove ignored directories
dirs_array = []
for x in os.walk(path):
    cur_path = x[0]
    if '.git' in cur_path:
        continue
    if '.idea' in cur_path:
        continue

    dirs_array.append(cur_path + '/')

all_project_files = []
all_php_filepaths = []
all_php_filenames = []
path_dict = dict()
# Generate array with every filename
for directory in dirs_array:
    all_files_in_dir = get_iterator_all_files_name(directory)
    all_project_files += all_files_in_dir

    # pega todos os arquivos do tipo PHP
    for file in all_files_in_dir:
        ext = file.rsplit('.', 1)[-1]
        if ext == 'php':
            all_php_filepaths.append(directory + file)
            all_php_filenames.append(file)

all_project_files.sort()
all_php_filepaths.sort()
unref_php_filenames = list(set(all_php_filenames))
unref_php_filenames.sort()

for file in all_php_filepaths:
    with open(file, 'r',  encoding='utf-8', errors='ignore') as open_file:
        file_string = open_file.read()

        for filename in unref_php_filenames:
            if filename in file_string:
                unref_php_filenames.remove(filename)


tree_dict = dict()
for directory in dirs_array:
    files_dict = dict()
    all_files_in_dir = get_iterator_all_files_name(directory)
    for each_file in all_files_in_dir:
        if '.php' not in each_file:
            continue

        check_ext = each_file.rsplit('.php', 1)[-1] != ''
        syntax = False
        pg_connect = False
        uploaded = False
        unref = False

        extension = each_file.rsplit('.', 1)[-1]  # recebe tipo da extensao

        if extension == 'php':
            # Loads file to variable as string
            with open(directory + each_file, 'r', encoding='utf-8', errors='ignore') as myfile:
                loaded_file = myfile.read()

                # Checks for comment lines and comment blocks and remove then to search only in code being used
                treated_file = re.sub(r"((/\*).*(\*/))|((/\*).*$)|(//[^\n]*)", '', loaded_file, flags=re.DOTALL)

                syntax = php_syntax_test(directory, each_file)
                pg_connect = 'pg_connect' in treated_file
                uploaded = 'move_uploaded_file' in treated_file

            unref = each_file in unref_php_filenames

        files_dict[each_file] = [check_ext, syntax, pg_connect, uploaded, unref]

    tree_dict[directory] = files_dict


for directory in tree_dict:
    # Hide directories without PHP files
    if not tree_dict[directory]:
        continue

    # Print directory name
    print(colored(directory, 'blue'))
    for file in tree_dict[directory]:
        errors = []
        warnings = []

        results = tree_dict[directory][file]
        if results[0]:
            errors.append('Extensão PHP inválida')
        if results[1]:
            errors.append('Erro na sintáxe')
        if results[2]:
            warnings.append('Utiliza função pg_connect')
        if results[3]:
            warnings.append('Salva arquivo no servidor')
        if results[4]:
            errors.append('Arquivo não referenciado')

        # Set file status color
        file_color = 'green'
        if errors:
            file_color = 'red'
        elif warnings:
            file_color = 'yellow'
        # Print filename
        print(colored('  - ' + file, file_color))

        # Print errors messages
        for error in errors:
            print('      ' + error)
        # Print warnings messages
        for warning in warnings:
            print('      ' + warning)





