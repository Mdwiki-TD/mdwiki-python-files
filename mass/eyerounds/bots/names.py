"""

from mass.eyerounds.bots.names import make_files_names

"""

import os
import sys
from newapi import printe



def get_image_extension(image_url) -> str:
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

def make_files_names(img_infos, numb) -> dict:
    names = {}
    # ---
    printe.output(f"___________\nMaking names for case {numb}:")
    # ---
    used_names = {}
    # ---
    duplict_names = {}
    # ---
    for image_url, image_name in img_infos.items():
        if image_name in duplict_names:
            duplict_names[image_name] += 1
        else:
            duplict_names[image_name] = 1
    # ---
    duplict_names = {key: value for key, value in duplict_names.items() if value > 1}
    # ---
    printe.output(f"Duplicate names: len(duplict_names) = {len(duplict_names)}")
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
        image_name = f"EyeRounds Case {numb}, {name}"
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
        return names
    # ---
    for image_name, count in used_names.items():
        if count > 1:
            printe.output(f"Image name [[{image_name}]] <<yellow>>used {count} times")
    # ---
    return names
