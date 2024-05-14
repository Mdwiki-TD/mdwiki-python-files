# -*- coding: utf-8 -*-
"""
write python code to do:
2. read images.json
3. for each item in images.json ({"chapter_name": { "url": "chapter_url", "images": { "image_url": "image_name", ...}}, ...})
* do def create_category(chapter_name)
* upload images to nccommons.org using def upload_image(chapter_name, image_url, image_name, chapter_url)

python3 I:/mdwiki/pybot/mass/eyerounds/up.py
python3 core8/pwb.py mass/eyerounds/up break ask


tfj run eyeroundsx --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/eyerounds/up"

"""

import sys
import os
import time
import json
# from tqdm import tqdm
from pathlib import Path
from nccommons import api

from newapi import printe
from newapi.ncc_page import CatDepth

from mass.eyerounds.bots.catbot import category_name
from mass.eyerounds.bots.url_to_title import urls_to_title
from mass.eyerounds.bots.set_bot import create_set
from mass.eyerounds.bots.category_bot import create_category # create_category(chapter_name, pages)
from mass.eyerounds.bots.names import make_files_names

# Specify the root folder
main_dir = Path(__file__).parent

pages = CatDepth("Category:EyeRounds", sitecode="www", family="nccommons", depth=2, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])
time.sleep(1)
print("time.sleep(1)")


def get_data() -> dict:
    with open(main_dir / "jsons/images.json", "r", encoding="utf-8") as f:
        dataimages = json.load(f)

    data_done = []
    data = {}
    for url, da in dataimages.items():
        if url.lower() in data_done:
            continue
        data_done.append(url.lower())
        data[url] = da

    data = dict(sorted(data.items(), key=lambda item: len(item[1]["images"]), reverse=True))

    # print how many has images and how many has no images
    printe.output(f"<<green>> Number of sections with images: {len([k for k, v in data.items() if len(v['images']) > 0])}")

    printe.output(f"<<green>> Number of sections with no images: {len([k for k, v in data.items() if len(v['images']) == 0])}")

    # print len of all images
    printe.output(f"<<green>> Number of images: {sum(len(v['images']) for k, v in data.items())}")

    return data

def make_image_text(category, image_url, chapter_url):
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
        "[[Category:EyeRounds images]]\n"
    )

    return image_text


def upload_image(category, image_url, image_name, chapter_url) -> bool:
    if f"File:{image_name}" in pages:
        printe.output(f"<<lightyellow>> File:{image_name} already exists")
        return "exists"
    # ---
    image_text = make_image_text(category, image_url, chapter_url)
    # ---
    upload = api.upload_by_url(image_name, image_text, image_url, comment="")
    # ---
    print(f"upload result: {upload}")

    return upload

def process_images(images_info, category, numb, chapter_url) -> dict:
    files = {}
    if category and "noup" not in sys.argv:
        # ---
        files_names = make_files_names(images_info, numb)
        # ---
        n = 0
        # ---
        # for image_url, image_name in tqdm(images_info.items(), desc="Uploading images", total=len(images_info.keys())):
        for image_url, image_name in files_names.items():
            n += 1

            print(f"Uploading image {n}/{len(images_info.keys())}: {image_name}")

            upload = upload_image(category, image_url, image_name, chapter_url)

            if upload:
                files[len(files) + 1] = image_name

    return files

def process_folder() -> None:
    data = get_data()
    # ---
    if "test" in sys.argv:
        url= "https://eyerounds.org/cases/164-Toric-IOL-exchange.htm"
        data = {url: data[url]}
    # ---
    done = []
    # ---
    for chapter_url, info_data in data.items():
        images_info = info_data.get("images", {})

        if not images_info:
            printe.output(f"<<lightyellow>> No images found for {chapter_url}")
            continue

        _title = info_data.get("title")

        cat, numb = category_name(chapter_url)

        print(f"Processing {cat}")
        if numb in done or chapter_url.lower() in done:
            continue

        done.append(numb)
        done.append(chapter_url.lower())

        # Create category
        category = create_category(cat, chapter_url, pages)
        # ---
        files = process_images(images_info, category, numb, chapter_url)
        # ---
        if files:
            create_set(cat, files)

        if "break" in sys.argv:
            break


if __name__ == "__main__":
    # Process all subfolders in the specified root folder
    process_folder()
