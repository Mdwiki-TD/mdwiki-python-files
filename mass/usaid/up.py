"""

tfj run upusaid --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/usaid/up"

python3 core8/pwb.py mass/usaid/up test ask

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

from mass.usaid.bots.set_bot import create_set
from mass.usaid.bots.category_bot import create_category  # create_category(album_name, pages)
from mass.usaid.bots.names import make_files_names

# Specify the root folder
main_dir = Path(__file__).parent

pages_images = CatDepth("Category:USAID images", sitecode="www", family="nccommons", depth=0, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])
pages = CatDepth("Category:USAID", sitecode="www", family="nccommons", depth=0, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])
time.sleep(1)
print("time.sleep(1)")


def make_image_text(category, image, album_url, album_id) -> str:
    # ---
    image_url = image["url_o"]
    # ---
    _, base_name = os.path.split(image_url)
    # ---
    description = image["description"]
    img_id = image["id"]
    # ---
    image_text = "== {{int:summary}} ==\n"

    image_text += (
        "{{Information\n"
        f"|Description =\n"
        f"* Description: {description}\n"
        f"* Album: [{album_url} {album_id}]\n"
        f"* Image id: {img_id}\n"
        f"* Image url: [{image_url} {base_name}]\n"
        f"|Date = \n"
        f"|Source = {album_url}\n"
        "|Author = [https://www.flickr.com/people/usaid_images/ USAID U.S. Agency for International Development]\n"
        "|Permission = http://creativecommons.org/licenses/by-nc/2.0/\n"
        "}}\n"
        "== {{int:license}} ==\n"
        "{{CC BY-NC 2.0}}\n"
        f"[[{category}]]\n"
        "[[Category:USAID images]]\n"
    )

    return image_text


def upload_image(category, image, image_name, album_url, album_id) -> bool:
    # ---
    image_url = image["url_o"]
    # ---
    image_text = make_image_text(category, image, album_url, album_id)
    # ---
    image_url = image_url.replace(" ", "%20")
    # ---
    upload = api.upload_by_url(image_name, image_text, image_url, comment="")
    # ---
    print(f"upload result: {upload}")

    return upload


def process_images(images_info, category, album_url, album_id, title) -> dict:
    files = {}
    if category and "noup" not in sys.argv:
        # ---
        imgs = {x["url_o"]: x["title"] for x in images_info.values()}
        # ---
        files_names = make_files_names(imgs, album_id, title)
        # ---
        n = 0
        # ---
        # for image_url, image_name in tqdm(images_info.items(), desc="Uploading images", total=len(images_info.keys())):
        for image in images_info.values():
            _image = {
                "id": "53099223842",
                "title": "Administrator Power at a Swearing-In Ceremony for David Hoffman as Mission Director for Uzbekistan",
                "description": "August 4, 2023 - USAID Administrator Samantha Power officiated the swearing-in of David Hoffman as the new Mission Director of USAID/Uzbekistan. The ceremony took place at USAID Offices in Washington, D.C., USA.",
                "url_o": "https://live.staticflickr.com/65535/53099223842_0ff47f6e23_o.jpg",
            }
            # ---
            image_url = image["url_o"]
            title = image["title"]
            image_name = files_names[image_url]
            # ---
            n += 1
            # ---
            if f"File:{image_name}" in pages_images:
                files[len(files) + 1] = image_name
                continue
            # ---
            print(f"Uploading image {n}/{len(images_info.keys())}: {image_name}")
            # ---
            upload = upload_image(category, image, image_name, album_url, album_id)

            if upload:
                files[len(files) + 1] = image_name

    return files


def process_folder() -> None:
    # ---
    with open(main_dir / "jsons/all_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # ---
    data = dict(sorted(data.items(), key=lambda x: len(x[1]["images"]), reverse=True))
    # ---
    if "test" in sys.argv:
        uu = "72177720310190418"
        data = {uu: data[uu]}
    # ---
    done = []
    # ---
    _data = {
        "72177720310316192": {
            "url": "https://www.flickr.com/photos/usaid_images/albums/72177720310316192/",
            "title": "Administrator Power at a Swearing-In Ceremony for David Hoffman as Mission Director for Uzbekistan",
            "images": {
                "1": {
                    "id": "53099223842",
                    "title": "Administrator Power at a Swearing-In Ceremony for David Hoffman as Mission Director for Uzbekistan",
                    "description": "August 4, 2023 - USAID Administrator Samantha Power officiated the swearing-in of David Hoffman as the new Mission Director of USAID/Uzbekistan. The ceremony took place at USAID Offices in Washington, D.C., USA.",
                    "url_o": "https://live.staticflickr.com/65535/53099223842_0ff47f6e23_o.jpg",
                }
            },
            "photo_count": 3,
            "id": "72177720310316192",
        }
    }
    # ---
    for album_info in data.values():
        images_info = album_info["images"]
        title = album_info["title"]
        album_id = album_info["id"]
        album_url = album_info["url"]
        # ---
        if not images_info:
            printe.output(f"<<lightyellow>> No images found for {album_url}")
            continue
        # ---
        cat = f"USAID Album: {title}"
        print(f"Processing {cat}")
        # ---
        if album_url.lower() in done:
            continue
        done.append(album_url.lower())
        # ---
        # Create category
        category = create_category(cat, album_url, album_id, pages)
        # ---
        files = process_images(images_info, category, album_url, album_id, title)
        # ---
        if files:
            create_set(cat, files)
        # ---
        if "break" in sys.argv:
            break


if __name__ == "__main__":
    # Process all subfolders in the specified root folder
    process_folder()
