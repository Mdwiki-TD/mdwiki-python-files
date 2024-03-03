import re


def update_docstring(file_path, updated_docstring):
    with open(file_path, 'r+') as file:
        content = file.read()
        file.seek(0)
        file.write(updated_docstring + '\n\n')
        file.write(content)

def remove_commented_code(file_path):
    pattern = r'#.*\n'
    with open(file_path, 'r+') as file:
        content = file.read()
        updated_content = re.sub(pattern, '', content)
        file.seek(0)
        file.write(updated_content)
        file.truncate()

# Update the docstring in auths_cats.py
file_path = 'md_core/auths_cats.py'
updated_docstring = """
This module contains functions related to authentication and categories.
"""

update_docstring(file_path, updated_docstring)

# Remove unnecessary commented out code in auths_cats.py
remove_commented_code(file_path)
