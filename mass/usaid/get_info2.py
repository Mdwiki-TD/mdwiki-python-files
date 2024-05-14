"""

python3 core8/pwb.py mass/usaid/get_info break
python3 core8/pwb.py mass/usaid/get_info test

tfj run usaid --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/usaid/get_info"

"""

import sys
import json
import re
import requests
from bs4 import BeautifulSoup
import tqdm
from newapi import printe
from pathlib import Path

main_dir = Path(__file__).parent
albums_file = main_dir / "jsons/albums.json"


with open(albums_file, "r") as file:
    albums_list = json.load(file)


def get_img_titles(album_id):
    url = f"https://www.flickr.com/services/rest/?method=flickr.photosets.getPhotos&photoset_id={album_id}&api_key=c74ac20e4105b3bd301d1400572d73ba&format=json&nojsoncallback=1"
    response = requests.get(url)

    if response.status_code != 200:
        printe.output(f"Failed to fetch content from {url}")
        return {}

    data = response.json()
    titles = {}
    for item in data["photoset"]["photo"]:
        titles[str(item["id"])] = item["title"]

    return titles


def extract_infos_from_url(x):
    # Print the URL being processed
    url = f"https://api.flickr.com/services/rest?extras=title,description,url_o&per_page=500&page=1&get_user_info=1&primary_photo_extras=url_o&photoset_id={x}&method=flickr.photosets.getPhotos&api_key=c74ac20e4105b3bd301d1400572d73ba&format=json&nojsoncallback=1"
    # ---
    printe.output(f"\t Processing URL: {url}")

    # Send a GET request to the URL and get the response
    response = requests.get(url)

    # Check if the response status code is 200 (OK)
    if response.status_code != 200:
        # Print an error message if the request failed
        printe.output(f"\t\t Failed to fetch content from {url}")

        # Return an empty dictionary
        return {}

    # Parse the HTML content of the response using BeautifulSoup
    json_data = response.json()
    json_data = json_data["photoset"]
    album_url = f"https://www.flickr.com/photos/usaid_images/albums/{x}/"
    data = {"url": album_url, "title": "", "images": {}, "photo_count": 0}

    data["id"] = json_data["id"]
    data["title"] = json_data["title"]
    data["total"] = json_data["total"]

    data["photo_count"] = len(json_data["photo"])
    # ---
    for item in json_data["photo"]:
        _item = {
            "id": "49945886736",
            "secret": "d97b3fdaa0",
            "server": "65535",
            "farm": 66,
            "title": "_DSC9754",
            "isprimary": "0",
            "ispublic": 1,
            "isfriend": 0,
            "isfamily": 0,
            "description": {"_content": "Ventilators provided by the U.S. Government are packaged prior to being shipped to El Salvador to assist the country with their ongoing COVID-19 response."},
            "url_o": "https://live.staticflickr.com/65535/49945886736_620b5ec5d2_o.jpg",
            "height_o": 7379,
            "width_o": 4922,
        }
        item["description"] = item["description"]["_content"]

        data["images"][len(data["images"]) + 1] = item
    # ---
    return data


def start() -> None:
    to_work = albums_list
    # ---
    with open(main_dir / "jsons/all_data.json", "r", encoding="utf-8") as file:
        all_data = json.load(file)
    # ---
    if "test" in sys.argv:
        to_work = ["72177720300058248"]
    # ---
    for n, x in enumerate(to_work):
        printe.output(f"Processing album {n}/{len(to_work)} id: {x}")
        # ---
        data = extract_infos_from_url(x)
        # ---
        # print(json.dumps(data, indent=2))
        # ---
        if x not in all_data:
            all_data[x] = data
        # ---
        x_file = main_dir / f"jsons/albums/{x}.json"
        # ---
        with open(x_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        # ---
        if "break" in sys.argv:
            break
    # ---
    with open(main_dir / "jsons/all_data.json", "w", encoding="utf-8") as file:
        json.dump(all_data, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    start()
