"""
from nccommons import fix_svg
# file_path = fix_svg.remove_svg_dtd(file_path)

"""
import os
import urllib.request
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
import xml.etree.ElementTree as ET

def remove_svg_dtd(file_path, url=""):
    """
    function to remove dtd tags like: <!DOCTYPE svg  PUBLIC '-//W3C//DTD SVG 1.0//EN'  'http://www.w3.org/Graphics/SVG/1.0/DTD/svg10.dtd'>
    """
    
    # If no file_path provided but a URL is provided, download the file
    if not file_path and url:
        file_path, _ = urllib.request.urlretrieve(url)
    
    # Parse the SVG file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Remove the DOCTYPE declaration
    for elem in root.iter():
        # if elem.tag.startswith('{http://www.w3.org/2000/svg}') and elem.text and elem.text.startswith('<!DOCTYPE svg'):
        if elem.text and elem.text.startswith('<!DOCTYPE svg'):
            elem.text = ''
    
    # Write the modified SVG to the file
    tree.write(file_path)

    return file_path

def remove_svg_dtd_o(file_path, url=""):
    """
    function to remove dtd tags like: <!DOCTYPE svg  PUBLIC '-//W3C//DTD SVG 1.0//EN'  'http://www.w3.org/Graphics/SVG/1.0/DTD/svg10.dtd'>
    Args:
        file_path (str): The path to the SVG file.
        url (str, optional): The URL of the SVG file if accessed remotely. Defaults to "".

    Returns:
        str: file_path
    """
    # If URL is provided, download the file
    if not file_path and url:
        file_path, _ = urllib.request.urlretrieve(url)
    
    # Open original file
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Remove the lines containing the DTD declaration
    lines = [line for line in lines if 'DOCTYPE svg' not in line]

    # Write the modified content to a temporary file
    fd, temp_path = mkstemp()
    with fdopen(fd, 'w') as tmp:
        tmp.writelines(lines)

    # Copy the file permissions from the original file
    copymode(file_path, temp_path)

    # Remove original file
    remove(file_path)

    # Move the modified file to the original file location
    move(temp_path, file_path)

    return file_path


if __name__ == '__main__':
    dpp = remove_svg_dtd("", url="")
