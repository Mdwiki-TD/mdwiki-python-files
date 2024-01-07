'''

python3 core8/pwb.py mass/radio/studies test

'''
import sys
import os
from pathlib import Path
from bs4 import BeautifulSoup
import re
import requests
import json

main_dir = Path(__file__).parent

# make dir studies
if not os.path.exists(os.path.join(str(main_dir), 'studies')):
    os.makedirs(os.path.join(str(main_dir), 'studies'))

ids_file = os.path.join(str(main_dir), 'jsons/ids.json')
with open(ids_file, 'r', encoding='utf-8') as f:
    ids = json.loads(f.read())

def get_images(url):
    print(f"url: {url}")

    response = requests.get(url)
    studies = []

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
        return '', studies

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # <a class="view-fullscreen-link" href="/cases/97085/studies/117071?lang=us">
    scripts = soup.find_all('script')
    
    image_info = []

    for script in scripts:
        text = script.text.strip()
        if text.find('stackedImages') != -1:
            match = re.search(r'var stackedImages = (.*?);', text)
            print('stackedImages:')
            if match:
                json_data = match.group(1)

                data = json.loads(json_data)

                for entry in data:
                    # { "id": 21152341, "fullscreen_filename": "https://prod-images-static.radiopaedia.org/images/21152341/f802b27c53bf577c1ab269b3ef526a_big_gallery.jpeg", "public_filename": "https://prod-images-static.radiopaedia.org/images/21152341/f802b27c53bf577c1ab269b3ef526a.png", "plane_projection": "Sagittal", "aux_modality": "T1", "position": 10, "content_type": "image/png", "width": 512, "height": 512, "show_feature": false, "show_pin": false, "show_case_key_image": false, "show_stack_key_image": false, "download_image_url": "/images/21152341/download?layout=false", "crop_pending": false }

                    for image in entry['images']:
                        image_info.append(image)
                    
    print(f'len image_info: {len(image_info)}')

    return image_info

def main():
    ids = {}

    with open(ids_file, 'r', encoding='utf-8') as f:
        ids = json.loads(f.read())

    n = 0
    for url, tab in ids.items():

        for study in tab['studies']:
            n += 1
            print(f"n: {n}/ f {len(ids)}")
            # study id
            st_id = study.split('/')[-1]
            st_file = os.path.join(str(main_dir), 'studies', f'{st_id}.json')
            #---
            if not os.path.exists(st_file):
                #---
                ux = get_images(study)
                #---
                with open(st_file, 'w', encoding='utf-8') as f:
                    json.dump(ux, f, ensure_ascii=False, indent=4)
                #---

if __name__ == "__main__":
    if 'test' in sys.argv:
        get_images('https://radiopaedia.org/cases/44130/studies/47697')
    else:
        main()
