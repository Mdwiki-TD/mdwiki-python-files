# -*- coding: utf-8 -*-
"""
write python code to do:
2. read images.json
3. for each item in images.json ({"chapter_name": { "url": "chapter_url", "images": { "image_url": "image_name", ...}}, ...})
* do def create_category(chapter_name)
* upload images to nccommons.org using def upload_image(chapter_name, image_url, image_name, chapter_url)

python3 I:/mdwiki/pybot/mass/eyerounds/up.py
python3 core8/pwb.py mass/eyerounds/up break

"""

import sys
import os
import time
import json
from tqdm import tqdm
from newapi import printe
from pathlib import Path
from nccommons import api
from newapi.ncc_page import CatDepth

from mass.eyerounds.bots.catbot import category_name
from mass.eyerounds.bots.url_to_title import urls_to_title
from mass.eyerounds.bots.set_bot import create_set

# Specify the root folder
main_dir = Path(__file__).parent

with open(main_dir / "jsons/images.json", "r", encoding="utf-8") as f:
    dataimages = json.load(f)

data_done = []
data = {}
for url, da in dataimages.items():
    if url in data_done:
        continue
    data_done.append(url)
    data[url] = da

data = dict(sorted(data.items(), key=lambda item: len(item[1]["images"]), reverse=True))

# print how many has images and how many has no images
printe.output(f"<<green>> Number of sections with images: {len([k for k, v in data.items() if len(v['images']) > 0])}")

printe.output(f"<<green>> Number of sections with no images: {len([k for k, v in data.items() if len(v['images']) == 0])}")

# print len of all images
printe.output(f"<<green>> Number of images: {sum(len(v['images']) for k, v in data.items())}")

done = []

pages = CatDepth("Category:EyeRounds", sitecode="www", family="nccommons", depth=2, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])
time.sleep(1)
print("time.sleep(1)")


def get_image_extension(image_url):
    # Split the URL to get the filename and extension
    _, filename = os.path.split(image_url)

    # Split the filename to get the name and extension
    name, extension = os.path.splitext(filename)

    # Return the extension (without the dot)
    return extension[1:]


def make_file(image_name, image_url):
    image_name = image_name.replace("_", " ").replace("  ", " ")
    # base_name = os.path.basename(image_url)

    # get image extension from image_url
    print(image_url)
    extension = get_image_extension(image_url)

    # add extension to image_name
    image_name = f"{image_name}.{extension}"
    image_name = image_name.replace("..", ".")
    return image_name


def create_category(chapter_name):
    cat_text = f"* Image set: [[{chapter_name}]]\n[[Category:EyeRounds]]"
    cat_title = f"Category:{chapter_name}"
    # ---
    if "nocat" in sys.argv:
        return cat_title
    # ---
    chapter_name = chapter_name.replace("_", " ").replace("  ", " ")
    if cat_title in pages:
        printe.output(f"<<lightyellow>>{cat_title} already exists")
        return cat_title
    # ---
    api.create_Page(cat_text, cat_title)
    # ---
    return cat_title


def upload_image(category, image_url, image_name, chapter_url):
    if f"File:{image_name}" in pages:
        printe.output(f"<<lightyellow>> File:{image_name} already exists")
        return
    # ---
    chapter_name = urls_to_title.get(chapter_url)
    # ---
    _, base_name = os.path.split(image_url)
    # ---
    image_text = "== {{int:summary}} ==\n"

    image_text += (
        "{{Information\n"
        f"|Description = \n"
        f"* EyeRounds chapter: [{chapter_url} {chapter_name}]\n"
        f"* Image url: [{image_url} {base_name}]\n"
        f"|Date = \n"
        f"|Source = {chapter_url}\n"
        "|Author = [https://eyerounds.org/cases.htm Undergraduate Diagnostic Imaging Fundamentals]\n"
        "|Permission = http://creativecommons.org/licenses/by-nc-sa/3.0/\n"
        "}}\n"
        "== {{int:license}} ==\n"
        "{{Cc-by-nc-nd-3.0}}\n"
        f"[[{category}]]\n"
        "[[Category:EyeRounds]]"
    )

    upload = api.upload_by_url(image_name, image_text, image_url, comment="")

    print(f"upload result: {upload}")


def process_folder():
    for chapter_url, info_data in data.items():
        images_info = info_data.get("images", {})
        title = info_data.get("title")

        cat, numb = category_name(chapter_url)

        print(f"Processing {cat}")
        # Create category
        files = []
        if images_info:
            category = create_category(cat)

            if category and "noup" not in sys.argv:
                # Upload images
                n = 0
                for image_url, image_name in tqdm(images_info.items(), desc="Uploading images", total=len(images_info.keys())):
                    n += 1

                    # add extension to image_name
                    image_name = make_file(image_name, image_url)

                    print(f"Uploading image {n}/{len(images_info.keys())}: {image_name}")
                    upload_image(category, image_url, image_name, chapter_url)

                    files.append(image_name)

            create_set(cat, files)

            if "break" in sys.argv:
                break


if __name__ == "__main__":
    # Process all subfolders in the specified root folder
    process_folder()
