# -*- coding: utf-8 -*-
"""

python3 core8/pwb.py mass/usaid/all_cats ask

"""
import json
from pathlib import Path
from newapi import printe
from newapi.ncc_page import MainPage as ncc_MainPage

# Specify the root folder
main_dir = Path(__file__).parent


def doo():
    with open(main_dir / "jsons/all_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # data = {"72157623336842886": { "url": "https://www.flickr.com/photos/usaid_images/albums/72157623336842886/", "title": "USAID Administrator Rajiv Shah", "images": [], "photo_count": 11 }}
    # sort data by len of images

    data = dict(sorted(data.items(), key=lambda x: len(x[1]["images"]), reverse=True))

    text = '{| class="wikitable sortable"\n|-\n' + "! # !! Category !! Image set !! Url!! photos count\n"
    # ---
    all_images = 0
    # ---
    for n, (album_id, tab) in enumerate(data.items(), start=1):
        # tab = { "url": "https://www.flickr.com/photos/usaid_images/albums/72157623336842886/", "title": "USAID Administrator Rajiv Shah", "images": [], "photo_count": 11 }
        # ---
        url   = tab["url"]
        title = tab["title"]
        count = tab["photo_count"]
        # ---
        cat = f"USAID Album: {title}"
        # ---
        all_images += count
        # ---
        text += "|- \n"
        text += f"! {n}\n"
        text += f"| [[:Category:{cat}]]\n"
        text += f"| [[{cat}|set]]\n"  # + '|| {{#ifexist:' + x2 + '|1|0}}\n'
        text += f"| [{url} {album_id}]\n"  # + '|| {{#ifexist:' + x2 + '|1|0}}\n'
        text += f"| {count}\n"
    # ---
    text += (
        "|-\n"
        "! #\n"
        "! \n"
        "! \n"
        "! \n"
        f"! {all_images}\n"
    )
    # ---
    text += "|}"
    text += "\n[[Category:USAID|*]]"

    page = ncc_MainPage("User:Mr._Ibrahem/USAID", "www", family="nccommons")
    # ---
    old_text = page.get_text()
    # ---
    if old_text != text:
        page.save(newtext=text, summary="update", nocreate=0, minor="")
    else:
        printe.output("<<lightyellow>> No changes")

if __name__ == "__main__":
    # Process all subfolders in the specified root folder
    doo()
