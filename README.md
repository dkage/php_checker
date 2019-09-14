# PHP project analyzer

This project was created to analyze PHP projects, given the directory of the project it follows recursively through each subdir inside it.

This script was created because at my workplace we had dozens of old legacy PHP web applications (some even used PHP 5.3), and the department director asked me to create a script to analyze those old projects and find pieces of code that we should alter or remove, to clean the projects from non-used php files, connections to databases without using our new database class and so on.

### What kind of thing is analyzed?

This script lookouts for the following things on given PHP project to iterate:

- **check syntax using php lint CLI to checks for files with errors** (php -l 'filename')
- **uses of _pg_connect_** (as we are now using a new database connection class that is more secure, we needed to find the old connections the used pg_connect to make the proper change to adapt the legacy projects)
- **files that are not index.php and are not being referenced anywhere in the project** (no 'include'/'require' and/or 'redirects'/'href' calls)
- **saves files to the server** (checks if PHP script uses a function to save file on server HD (upload by user), as our new security guidelines demands that every file should be stored in a specific folder we needed to check for older scripts that save those files in other directories)

### How to use

To use the script you need to call it on CLI using Python3.

You need to install _colorterm_ package using PIP3 first, as the output is presented on terminal using different colors for better visualization of 'positives':

```pip3 install colorterm```

Then you can run the script and analyze a PHP project:

```python3 report_project.py <full_php_project_path>```

The output will be the name of files with their full_path followed by the errors/warnings found, colored depending on the problems encountered. 

If you want the output without the colors you should just put a second parameter so you can put the output in a file without the color coding breaking the text.

```python3 report_project.py <full_php_project_path> no_color > test.txt```


[1] Obs.: This does not alter any file inside the project, just run through the directory and its subdirs to analyze for the listed problems.

[2] Obs.: This gives some false positives, the pointed files with error should be manually checked.

