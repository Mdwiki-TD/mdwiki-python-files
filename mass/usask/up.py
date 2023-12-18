# -*- coding: utf-8 -*-
"""
write python code to do:
2. read images.json
3. for each item in images.json ({"chapter_name": { "url": "chapter_url", "images": { "image_url": "image_name", ...}}, ...})
* do def create_category(chapter_name)
* upload images to nccommons.org using def upload_image(chapter_name, image_url, image_name, chapter_url)

python3 core8/pwb.py mass/usask/up ask

"""
import sys
import os
import time
import json
from tqdm import tqdm
from new_api import printe
from pathlib import Path
from nccommons import api
from new_api.ncc_page import CatDepth

# Specify the root folder
main_dir = Path(__file__).parent

with open(os.path.join(str(main_dir), 'images.json'), 'r') as f:
    data = json.load(f)

# print how many has images and how many has no images
printe.output(f"<<green>> Number of sections with images: {len([k for k, v in data.items() if len(v['images']) > 0])}")

printe.output(f"<<green>> Number of sections with no images: {len([k for k, v in data.items() if len(v['images']) == 0])}")

# print len of all images
printe.output(f"<<green>> Number of images: {sum([len(v['images']) for k, v in data.items()])}")

done = []

pages = CatDepth('Category:UndergradImaging', sitecode='www', family="nccommons", depth=1, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])
time.sleep(5)
print('time.sleep(5)')
len_all_images = []


def create_set(chapter_name, image_infos):
    title = chapter_name
    text = ''
    # ---
    if 'noset' in sys.argv:
        return
    # ---
    title = title.replace('_', ' ').replace('  ', ' ')
    if title in pages:
        printe.output(f'<<lightyellow>>{title} already exists')
        return
    # ---
    text += '{{Imagestack\n|width=850\n'
    text += f'|title={chapter_name}\n|align=centre\n|loop=no\n'
    # ---

    # for image_name, image_url in image_infos.items():
    for image_name in image_infos.keys():
        # |File:Pediculosis Palpebrarum (Dermatology Atlas 1).jpg|
        text += f'|File:{image_name}|\n'
    text += '\n}}\n[[Category:Image set]]\n'
    text += f'[[Category:{chapter_name}|*]]'
    # ---
    new = api.create_Page(text, title)
    # ---
    return new


def create_category(chapter_name):
    cat_text = f'* Image set: [[{chapter_name}]]\n[[Category:UndergradImaging]]'
    cat_title = f'Category:{chapter_name}'
    # ---
    if 'nocat' in sys.argv:
        return cat_title
    # ---
    chapter_name = chapter_name.replace('_', ' ').replace('  ', ' ')
    if cat_title in pages:
        printe.output(f'<<lightyellow>>{cat_title} already exists')
        return
    # ---
    api.create_Page(cat_text, cat_title)
    # ---
    return cat_title


def upload_image(category, image_url, image_name, chapter_url, chapter_name):
    global len_all_images
    # split chapter_url to get last text after =
    image_name = image_name.replace('_', ' ').replace('  ', ' ')
    len_all_images.append(image_name)

    if f'File:{image_name}' in pages:
        printe.output(f'<<lightyellow>> File:{image_name} already exists')
        return
    # ---
    image_text = '== {{int:summary}} ==\n'
    # get image base name
    base_name = os.path.basename(image_name)

    image_text += (
        '{{Information\n'
        f'|Description = \n'
        f'* UndergradImaging chapter: [{chapter_url} {chapter_name}]\n'
        f'* Image url: [{image_url} {base_name}]\n'
        f'|Date = \n'
        f'|Source = {chapter_url}\n'
        '|Author = [https://openpress.usask.ca/undergradimaging/ Undergraduate Diagnostic Imaging Fundamentals]\n'
        '|Permission = http://creativecommons.org/licenses/by-nc-sa/3.0/\n'
        '}}\n'
        '== {{int:license}} ==\n'
        '{{CC-BY-NC-SA-4.0}}\n'
        f'[[{category}]]\n'
        '[[Category:UndergradImaging]]'
    )

    upload = api.upload_by_url(image_name, image_text, image_url, comment='')

    print(f"upload result: {upload}")


def process_folder():

    with open(os.path.join(str(main_dir), 'images.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)

    for chapter_name, info_data in data.items():
        images_info = info_data.get("images", {})
        chapter_url = info_data.get("url")

        chapter_name2 = f'{chapter_name} (UndergradImaging)'
        print(f'Processing {chapter_name2}')
        # Create category
        category = create_category(chapter_name2)

        if category and 'noup' not in sys.argv:
            # Upload images
            n = 0
            for image_url, image_name in tqdm(images_info.items(), desc="Uploading images", total=len(images_info.keys())):
                n += 1
                print(f"Uploading image {n}/{len(images_info.keys())}: {image_name}")
                upload_image(category, image_url, image_name, chapter_url, chapter_name)

        create_set(chapter_name2, images_info)
        if 'break' in sys.argv:
            break

if __name__ == "__main__":
    # Process all subfolders in the specified root folder
    process_folder()
