# -*- coding: utf-8 -*-
"""
Usage:
python3 core8/pwb.py mass/eyerounds/getimages break

"""
import sys
import json
from pathlib import Path
from mass.eyerounds.bots.get_case_info import extract_infos_from_url
from newapi import printe

main_dir = Path(__file__).parent
jsonfile = main_dir / 'jsons/urls.json'
jsonimages = main_dir / 'jsons/images.json'

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def dump_data(json_data):
    # sort json_data by len of images
    json_data = dict(sorted(json_data.items(), key=lambda item: len(item[1].get("images", [])), reverse=True))

    if 'test' not in sys.argv:
        # Save the updated json_data back to the JSON file
        with open(jsonimages, 'w', encoding="utf-8") as file:
            json.dump(json_data, file, indent=2)

def get_images(json_data):
    # ---
    json_data = read_json_file(jsonimages)
    # ---
    data = json_data.copy()
    # ---
    if "onlyempty" in sys.argv:
        data = {k: v for k, v in data.items() if len(v.get("images", [])) == 0}
        printe.output(f"<<green>> Only {len(data)} urls have no images, from {len(data)} ")
    # ---
    # [ { "title": "Cataract", "url": "https://eyerounds.org/cataract_cases.htm", "cases": [ { "url": "https://eyerounds.org/cases/254-anterior-chamber-cilium.htm", ... } ] }, ... ]
    # ---
    # Iterate over each section and its corresponding data
    for n, (url, _tab) in enumerate(data.items(), 1):
        printe.output(f"<<yellow>> Processing section {n}/{len(data)}: {url}")

        d_in = json_data.get(url, {}).get("images", {})
        if d_in and "donew" not in sys.argv:
            printe.output(f"<<green>> Found {len(d_in)} images in json")
            continue

        # Extract images from the URL
        # { "authors": {}, "date": "", "images": {} }
        if not url.startswith("https://eyerounds.org/cases/"):
            printe.output(f"<<red>> Skip url {url}")
            continue
        case_info = extract_infos_from_url(url)

        printe.output(f"<<green>> Found {len(case_info['images'])} images in url {url}")

        json_data[url] = case_info

        if 'break' in sys.argv:
            print(json.dumps(case_info, indent=2))
            break

        if n % 50 == 0:
            dump_data(json_data)
    # ---
    dump_data(json_data)
    # ---
    return json_data

def main():
    # Read the JSON file
    data = read_json_file(jsonfile)

    cases_urls = read_json_file(jsonimages)

    for _, d in data.items():
        for x in d["cases"]:
            if x["url"] not in cases_urls:
                cases_urls[x["url"]] = { "authors": {}, "date": "", "images": {} }
    # ---
    url_by_images = get_images(cases_urls)
    # ---
    # print how many has images and how many has no images
    d_with = [k for k, v in url_by_images.items() if len(v["images"]) > 0]
    printe.output(f"<<green>> Number of sections with images: {len(d_with)}")

    d_no = [k for k, v in url_by_images.items() if len(v["images"]) == 0]
    printe.output(f"<<green>> Number of sections with no images: {len(d_no)}")

    # print len of all images
    d_all = sum(len(v["images"]) for k, v in url_by_images.items())
    printe.output(f"<<green>> Number of images: {d_all}")


if __name__ == "__main__":
    main()
