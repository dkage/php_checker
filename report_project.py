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

    return files_in_dir


def php_syntax_test(php_path, php_file):
    """Checks php file for syntax errors using php -lint"""
    cli_command = 'php -l ' + php_path + php_file + ' >/dev/null 2>&1'
    lint = os.system(cli_command)
    return lint != 0


# INPUT
# Check if parameter has been passed on .py execution command
if len(sys.argv) == 1:
    print('Insira o caminho absoluto do diretorio a ser analisado como parametro na chamada do script')
    print('Caso deseje remover as cores dos prints no terminal adicionar parametro "no_color" como parametro'
          ' apos o diretorio')
    sys.exit()

# Variable 'path' = to be analyzed project root folder - absolute path
path = sys.argv[1]

# Second variable (could actually be anything, not only no_color), sets to "file_mode" to save on file.
# In other words, set the output to not color the prints because it only works right for terminal output.
to_file_mode = sys.argv[2] if len(sys.argv) >= 3 else ''

# Check if the directory exists
if not os.path.isdir(path):
    print('Diretorio nao encontrado')
    sys.exit()

# END INPUT

print('Analisando arquivos...\n\n')


# Create array with every directory and subdirs and remove ignored directories (.git, .idea [if needed add more here])
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

    # Generate array with all PHP files and filenames
    for file in all_files_in_dir:
        ext = file.rsplit('.', 1)[-1]
        if ext == 'php':
            all_php_filepaths.append(directory + file)
            all_php_filenames.append(file)

all_project_files.sort()
all_php_filepaths.sort()

# Create a set with all PHP files without a found reference
unref_php_filenames = list(set(all_php_filenames))
unref_php_filenames.sort()

# This loop structure open and loads each PHP file on a string, then searches inside it for each PHP filename stored
# inside 'unref_php_filenames' array, if filename is found it probably means it is being used (include or redirects)
# and is taken out of the array, only the filenames without references stays on 'unref_php_filenames' array
for file in all_php_filepaths:
    with open(file, 'r',  encoding='utf-8', errors='ignore') as open_file:
        file_string = open_file.read()
        # Removes all comments to remove false positive where files are being referenced inside comment sections
        treated_file_string = re.sub(r"((/\*).*(\*/))|((/\*).*$)|(//[^\n]*)", '', file_string, flags=re.DOTALL)

        for filename in unref_php_filenames:
            # Remove filename from the list if a reference is found to optimize the next iterations
            if filename in treated_file_string:
                unref_php_filenames.remove(filename)


tree_dict = dict()
for directory in dirs_array:
    files_dict = dict()

    all_files_in_dir = get_iterator_all_files_name(directory)
    for each_file in all_files_in_dir:
        # Ignore files without '.php' in the filename
        if '.php' not in each_file:
            continue

        # Check if the file has an unvalid php extension
        check_ext = each_file.rsplit('.php', 1)[-1] != ''

        syntax = False
        pg_connect = False
        uploaded = False
        unref = False

        # Get file extension
        extension = each_file.rsplit('.', 1)[-1]  # recebe tipo da extensao

        if extension == 'php':
            # Load file to variable as string
            with open(directory + each_file, 'r', encoding='utf-8', errors='ignore') as myfile:
                loaded_file = myfile.read()

                # Check for comment lines and comment blocks and remove then to search only in code being used
                treated_file = re.sub(r"((/\*).*(\*/))|((/\*).*$)|(//[^\n]*)", '', loaded_file, flags=re.DOTALL)

                # Perform a syntax test on the file
                syntax = php_syntax_test(directory, each_file)

                # Search for uses of the 'pg_connect' function
                pg_connect = 'pg_connect' in treated_file

                # Search for uses of the 'move_uploaded_file' function
                uploaded = 'move_uploaded_file' in treated_file

            # Check if file in the unreferenced files list
            unref = each_file in unref_php_filenames

        # Store tests results
        files_dict[each_file] = [check_ext, syntax, pg_connect, uploaded, unref]

    tree_dict[directory] = files_dict


# OUTPUT

for directory in tree_dict:
    # Hides all directories without PHP files
    if not tree_dict[directory]:
        continue

    # Print directory name
    print('\n\n')
    if to_file_mode:
        print(directory)
    else:
        print(colored(directory, 'blue'))
    for file in tree_dict[directory]:
        errors = []
        warnings = []

        # Create messages based on the tests results
        results = tree_dict[directory][file]
        if results[0]:
            errors.append('Extensao PHP invalida')
        if results[1]:
            errors.append('Erro na sintaxe')
        if results[2]:
            warnings.append('Utiliza funcao pg_connect')
        if results[3]:
            warnings.append('Salva arquivo no servidor')
        if results[4]:
            errors.append('Arquivo nao referenciado')

        # Set file status color
        file_color = 'green'
        if errors:
            file_color = 'red'
        elif warnings:
            file_color = 'yellow'

        # If file_mode active, then all colors all removed or color codes will break the text
        if to_file_mode:
            file_color = ''
        # Print filename
        if to_file_mode:
            output = directory + file
        else:
            output = colored(directory + file, file_color)

        # Print errors messages
        for error in errors:
            output += '  -  ' + error


        # Print warnings messages
        for warning in warnings:
            output += '  -  ' + warning

        print(output)
# END OUTPUT
