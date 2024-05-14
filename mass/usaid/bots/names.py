"""

from mass.eyerounds.bots.names import make_files_names

"""

import os
import sys
from newapi import printe



def get_image_extension(image_url) -> tuple:
    # Split the URL to get the filename and extension
    _, filename = os.path.split(image_url)

    # Split the filename to get the name and extension
    name, extension = os.path.splitext(filename)

    # Return the extension (without the dot)
    return name, extension[1:]


def make_file(image_name, image_url) -> str:
    # base_name = os.path.basename(image_url)

    # get image extension from image_url
    # print(image_url)
    name, extension = get_image_extension(image_url)

    if not image_name:
        image_name = name

    # add extension to image_name
    image_name = f"{image_name}.{extension}"
    image_name = image_name.replace("..", ".")
    return image_name

def make_files_names(img_infos, album_id, title) -> dict:
    names = {}
    # ---
    printe.output(f"___________\nMaking names for {album_id}:")
    # ---
    used_names = {}
    # ---
    numb = 0
    # ---
    for image_url, img_name in img_infos.items():
        # add extension to image_name
        # ---
        img_name = img_name.strip()
        img_name = img_name.replace("_", " ").replace("  ", " ")
        # ---
        # image_name = make_file(img_name, image_url)
        # ---
        name, extension = get_image_extension(image_url)
        # ---
        name = name.replace("_", " ").replace("  ", " ")
        # ---
        # check if extension is valid media type
        if extension.lower() not in ["jpg", "jpeg", "png", "gif", "svg"]:
            printe.output(f"Invalid extension: {extension}")
            continue
        # ---
        numb += 1
        # ---
        image_name = f"USAID Album {album_id}, image {numb}"
        # ---
        image_name = f"{image_name}.{extension}"
        image_name = image_name.replace("..", ".")
        # ---
        used_names.setdefault(image_name, 0)
        used_names[image_name] += 1
        # ---
        names[image_url] = image_name
    # ---
    if len(list(set(names.values()))) == len(names):
        printe.output("<<green>> All image names are unique")
    # ---
    return names
