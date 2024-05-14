"""
python3 core8/pwb.py mass/eyerounds/mk_names

"""

import sys
import json
from pathlib import Path

from newapi import printe

from mass.eyerounds.bots.catbot import category_name
from mass.eyerounds.bots.url_to_title import urls_to_title
from mass.eyerounds.bots.names import make_files_names

# Specify the root folder
main_dir = Path(__file__).parent


def get_data() -> dict:
    with open(main_dir / "jsons/images.json", "r", encoding="utf-8") as f:
        dataimages = json.load(f)

    data_done = []
    data = {}
    for url, da in dataimages.items():
        if url in data_done:
            continue
        data_done.append(url)
        data[url] = da

    return data


def process_folder(data) -> None:
    # ---
    new_data = {}
    # ---
    for chapter_url, info_data in data.items():
        images_info = info_data.get("images", {})

        if not images_info:
            printe.output(f"<<lightyellow>> No images found for {chapter_url}")
            continue

        _cat, numb = category_name(chapter_url)
        # ---
        files_names = make_files_names(images_info, numb)
        # ---
        new_data[chapter_url] = {"number": numb, "files_names": files_names}
        # ---
        print(json.dumps(new_data, indent=2))
    # ---


def start() -> None:
    data = get_data()
    # ---
    if "test" in sys.argv:
        urls = [
            # "https://eyerounds.org/cases/43-Corneal-Stromal-Dystrophies.htm",
            # "https://eyerounds.org/cases/195-Behcets.htm",
            # "https://eyerounds.org/cases/83-Presumed-Ocular-Histoplasmosis-POHS.htm",
            "https://eyerounds.org/cases/211-Aniridia.htm",
        ]
        new_data = {}
        for url in urls:
            if url in data:
                new_data[url] = data[url]
        data = new_data
    # ---
    process_folder(data)


if __name__ == "__main__":
    # Process all subfolders in the specified root folder
    start()
