# -*- coding: utf-8 -*-
"""
Usage:
python3 I:/mdwiki/pybot/mass/usask/getimages.py
python3 core8/pwb.py mass/usask/getimages
write python code to do:

main_dir = Path(__file__).parent
jsonfile = os.path.join(str(main_dir), 'urls.json')

1. read file jsonfile and get all urls
# { "Foreword": { "url": "https://openpress.usask.ca/undergradimaging/front-matter/introduction/", "images": {} }, ... }

2. for each url in urls do:
    * open url
    * get all figure tags like: (<figure id="attachment_1081" aria-describedby="caption-attachment-1081" style="width: 600px"
    class="wp-caption aligncenter">...</figure>)
    * get the caption from figcaption tag like: (<figcaption>...</figcaption>)
    * get the image "srcset" from img tag
        (srcset="https://openpress.usask.ca/app/uploads/sites/34/2019/02/ODIN-image-viewing-pane-300x238.jpg 300w, https://openpress.usask.ca/app/uploads/sites/34/2019/02/ODIN-image-viewing-pane-768x609.jpg 768w, ..")
    * store the image url in images dictionary like: {"image_url": "caption"}
"""

import re
import sys
import os
import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup
# ---
from new_api import printe
# ---

main_dir = Path(__file__).parent
jsonfile = os.path.join(str(main_dir), 'urls.json')
jsonimages = os.path.join(str(main_dir), 'images.json')


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_images_from_url(url):
    # Print the URL being processed
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
    soup = BeautifulSoup(response.text, 'html.parser')

    # Create a dictionary to store the image URLs and their captions
    images_info = {}

    # Find all 'figure' tags in the HTML
    figure_tags = soup.find_all('figure')

    # Iterate over each 'figure' tag
    for n, figure_tag in enumerate(figure_tags):
        printe.output(f'\t<<purple>> >> figure {n+1}/{len(figure_tags)}')
        # Find the 'figcaption' tag within the 'figure' tag
        caption_tag = figure_tag.find('figcaption')

        # Get the text of the 'figcaption' tag and remove leading/trailing whitespaces
        caption = caption_tag.text.strip() if caption_tag else ""
        printe.output(f'\t\t <<yellow>> caption: <<default>> {caption}')
        # Find the 'img' tag within the 'figure' tag
        img_tag = figure_tag.find('img')

        # Check if 'img' tag exists
        if img_tag:
            # Get the value of the 'srcset' attribute of the 'img' tag
            img_srcset = img_tag.get('srcset', '').split(',')[0].split()[0] if img_tag.get('srcset', '') else ''
            img_src    = img_tag.get('src', '')
            # printe.output(f'\t\t <<yellow>> img_srcset: <<default>> {img_srcset}')
            # printe.output(f'\t\t <<yellow>> img_src: <<default>> {img_src}')
            # Split the 'srcset' value by comma and get the first URL
            img_url = img_srcset
            if not img_srcset:
                img_url = img_src
                printe.output(f'\t\t <<red>> no srcset, use src')
        
            # Remove the dimension part from the URL using regex
            img_url = re.sub(r'-\d+x\d+(\.\w+)$', r'\1', img_url)
            printe.output(f'\t\t <<yellow>> img_url: <<default>> {img_url}')

            # Check if a valid image URL exists
            if img_url:
                # Add the image URL and its caption to the dictionary
                images_info[img_url] = caption

    # Return the dictionary containing the image URLs and captions
    return images_info


def main():
    # Read the JSON file
    data = read_json_file(jsonfile)

    # If 'test' is in the command line arguments, replace data with a test value
    if 'test' in sys.argv:
        data = {
            "Online DICOM Image Viewer (ODIN): An Introduction and User Manual": {
                "url": "https://openpress.usask.ca/undergradimaging/chapter/online-dicom-image-viewer-odin-an-introduction-and-user-manual/",
                "images": {}
            }
        }

    # Initialize a counter
    n = 0

    # Iterate over each section and its corresponding data
    for section, section_data in data.items():
        # Increment the counter
        n += 1

        # Print the section being processed
        printe.output(f"<<yellow>> Processing section {n}/{len(data)}: {section}")

        # Get the URL from the section data
        url = section_data['url']

        # Extract images from the URL
        images_info = extract_images_from_url(url)

        # If images are found, update the data with the extracted image information
        if images_info:
            data[section]['images'] = images_info

    # If 'test' is in the command line arguments, print the updated data
    if 'test' in sys.argv:
        printe.output('')
        # printe.output(json.dumps(data, indent=2))
    else:
        # Save the updated data back to the JSON file
        with open(jsonimages, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=2)


if __name__ == "__main__":
    main()
