import os
import re


def update_readme():
    # Read the contents of the existing README.md file
    with open("README.md", "r") as f:
        readme_content = f.read()

    # Add a description of the new features and any new commands that have been added
    new_features = """
    New Features:
    - Feature 1: Description of feature 1.
    - Feature 2: Description of feature 2.
    
    New Commands:
    - Command 1: Description of command 1.
    - Command 2: Description of command 2.
    """

    # Update the README.md file with the new content
    updated_content = re.sub(r"(?<=## Features\n)", new_features, readme_content)

    # Write the updated README.md content back to the file
    with open("README.md", "w") as f:
        f.write(updated_content)

# Call the function to update the README.md file
update_readme()
