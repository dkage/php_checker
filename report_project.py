import os

path = '/Users/danilo/Sites/localhost/wwwroot/educfinAdm/'
relative_path = '/'


def get_iterator_all_files_name(dir_path):
    files_path = os.listdir(dir_path)
    # dirs_path = [x[0] for x in os.walk(path)]
    return files_path


files = get_iterator_all_files_name(path)

files.sort()
for file in files:
    if os.path.isdir(path + file) or file == '.gitlab-ci.yml':
        continue
    extension = file.rsplit('.', 1)[-1]
    if extension == 'php':
        cli_command = 'php -l ' + path + file + ' >/dev/null 2>&1'
        # cli_command = 'php -l ' + file
        lint = os.system(cli_command)
        output = relative_path + file + '   ' + ('OK' if lint == 0 else 'SYNTAX ERROR')
    print(output)
