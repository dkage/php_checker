# PHP project analyzer

This project was created to analyze PHP projects, given the directory of the project it follows through each subdir inside it.

This script basically lookout for the following things inside PHP files:

- **check syntax using php lint CLI** (php -l 'filename')
- **uses of _pg_connect_** (we started using our own database class for connection and needed to change the legacy files)
- **files that are not index.php and are not being referenced anywhere in the project** (no 'include' and/or 'redirects' calls)
- **saves files to the server** (so we are able to check if the folder that the legacy applications are saving to follows our new security guidelines and permissions)

To use the script you need to call it on CLI using Python3.

You need to install _colorterm_ package using PIP3 first:

```pip3 install colorterm```

Then you can run the script:

```python3 report_project.py <full_php_project_path>```

The output will be the name of files with their full_path followed by the errors/warnings found, colored depending on the problems found. But if you want the output without the colors you should just put a second parameter so you can put the output in a file without the color coding breaking the text.

```python3 report_project.py <full_php_project_path> no_color > test.txt```


Obs.: This does not alter any file inside the project, just run through the directory and its subdirs to analyze for the listed problems.

