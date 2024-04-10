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
jsonfile = main_dir / 'urls.json'
jsonimages = main_dir / 'images.json'

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_images(data):
    # ---
    json_data = read_json_file(jsonimages)
    # ---
    added = { x : { "authors": {}, "date": "", "images": {} } for x in data if x not in json_data }
    if added:
        printe.output(f"<<green>> added {len(added)} new urls to json")
        json_data.update(added)
    # ---
    # [ { "title": "Cataract", "url": "https://eyerounds.org/cataract_cases.htm", "cases": [ { "url": "https://eyerounds.org/cases/254-anterior-chamber-cilium.htm", ... } ] }, ... ]
    # ---
    # Iterate over each section and its corresponding data
    for n, url in enumerate(data, 1):
        printe.output(f"<<yellow>> Processing section {n}/{len(data)}: {url}")

        d_in = json_data.get(url, {}).get("images", {})
        if d_in and "donew" not in sys.argv:
            printe.output(f"<<green>> Found {len(d_in)} images in json")
            continue
    
        # Extract images from the URL
        # { "authors": {}, "date": "", "images": {} }
        case_info = extract_infos_from_url(url)

        printe.output(f"<<green>> Found {len(case_info['images'])} images in url {url}")

        json_data[url] = case_info
        
        if 'break' in sys.argv:
            print(json.dumps(case_info, indent=4))
            break
    # ---
    return json_data

def main():
    # Read the JSON file
    data = read_json_file(jsonfile)
    
    cases_urls = {}

    for _, d in data.items():
        cases_urls.update({ x["url"] : {} for x in d["cases"] })
    
    if "urlkeys" in sys.argv:
        with open(jsonimages, 'w', encoding="utf-8") as file:
            json.dump(cases_urls, file, indent=2)

    url_by_images = get_images(cases_urls)
    # ---
    for x, va in url_by_images.copy().items():
        if not va:
            url_by_images[x] = { "authors": {}, "date": "", "images": {} }
    # ---
    # sort url_by_images by len of images
    url_by_images = dict(sorted(url_by_images.items(), key=lambda item: len(item[1].get("images", [])), reverse=True))
    
    if 'test' not in sys.argv:
        # Save the updated url_by_images back to the JSON file
        with open(jsonimages, 'w', encoding="utf-8") as file:
            json.dump(url_by_images, file, indent=2)

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
