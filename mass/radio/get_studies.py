"""

python3 core8/pwb.py mass/radio/get_studies test

from mass.radio.get_studies import get_stacks_fixed#(study_id, case_id, get_cach=False)

"""
import os
import re
import requests
import json
from pathlib import Path
from bs4 import BeautifulSoup
from newapi import printe

from mass.radio.jsons_files import jsons, urls_to_ids


main_dir = Path(__file__).parent
# ---
studies_dir = Path("/data/project/mdwiki/studies")
# ---
if str(main_dir).find("/mnt/nfs/labstore-secondary-tools-project/ncc") != -1:
    studies_dir = Path("/data/project/ncc/studies")
    printe.output(f"<<red>> studies_dir set to {studies_dir}")
# ---
if not os.path.exists(studies_dir):
    printe.output(f"<<red>> studies_dir {studies_dir} not found")
    studies_dir = main_dir / "studies"
    printe.output(f"<<red>> studies_dir set to {studies_dir}")


def dump_it(study_id, data):
    # ---
    st_file = studies_dir / f"{study_id}.json"
    # ---
    with open(st_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        printe.output(f"<<green>> get_studies: write {len(data)} to file: {st_file}")


def get_studies_from_cach(study_id):
    # ---
    st_file = studies_dir / f"{study_id}.json"
    # ---
    if st_file.exists():
        printe.output(f"<<green>> get_studies: get_cach: {st_file} exists")
        try:
            with open(st_file, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            printe.output(f"<<red>> get_studies: get_cach: {st_file} error: {e}")
            return {}
    # ---
    return {}


def get_images(url):
    print(f"url: {url}")
    # ---
    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        print(f"Failed to retrieve content from the URL. Error: {e}")
        return "", []

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
        studies = []

        return "", studies

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    # <a class="view-fullscreen-link" href="/cases/97085/studies/117071?lang=us">
    scripts = soup.find_all("script")

    image_info = []

    for script in scripts:
        text = script.text.strip()
        if text.find("stackedImages") != -1:
            match = re.search(r"var stackedImages = (.*?);", text)
            print("stackedImages:")
            if match:
                data = json.loads(match.group(1))
                for entry in data:
                    modality = entry.get("modality")
                    # { "id": 21152341, "fullscreen_filename": "https://prod-images-static.radiopaedia.org/images/21152341/f802b27c53bf577c1ab269b3ef526a_big_gallery.jpeg", "public_filename": "https://prod-images-static.radiopaedia.org/images/21152341/f802b27c53bf577c1ab269b3ef526a.png", "plane_projection": "Sagittal", "aux_modality": "T1", "position": 10, "content_type": "image/png", "width": 512, "height": 512, "show_feature": false, "show_pin": false, "show_case_key_image": false, "show_stack_key_image": false, "download_image_url": "/images/21152341/download?layout=false", "crop_pending": false }
                    images = entry.get("images")
                    for image in images:
                        if not image.get("modality", "") and modality:
                            image["modality"] = modality
                        image_info.append(image)

    printe.output(f"<<green>> len image_info: {len(image_info)}")
    # sort images by "id"
    image_info = sorted(image_info, key=lambda x: x["id"])
    return image_info


def get_images_stacks(study_id):
    new_url = f"https://radiopaedia.org/studies/{study_id}/stacks"
    print(f"get_images_stacks: study_id: {study_id}, new_url: {new_url}")
    # ---
    image_info = []
    # ---
    try:
        response = requests.get(new_url, timeout=10)
    except Exception as e:
        print(f"Failed to retrieve content from the URL. Error: {e}")
        return image_info
    # ---

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
        return image_info

    text = response.text
    if not text.startswith("[") and not text.endswith("]"):
        print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
        return image_info

    json_data = json.loads(text)
    for entry in json_data:
        modality = entry.get("modality")
        # { "id": 21152341, "fullscreen_filename": "https://prod-images-static.radiopaedia.org/images/21152341/f802b27c53bf577c1ab269b3ef526a_big_gallery.jpeg", "public_filename": "https://prod-images-static.radiopaedia.org/images/21152341/f802b27c53bf577c1ab269b3ef526a.png", "plane_projection": "Sagittal", "aux_modality": "T1", "position": 10, "content_type": "image/png", "width": 512, "height": 512, "show_feature": false, "show_pin": false, "show_case_key_image": false, "show_stack_key_image": false, "download_image_url": "/images/21152341/download?layout=false", "crop_pending": false }
        images = entry.get("images")
        for image in images:
            if not image.get("modality", "") and modality:
                image["modality"] = modality
            image_info.append(image)

    printe.output(f"<<green>> len image_info: {len(image_info)}")

    # sort images by "id"
    # image_info = sorted(image_info, key=lambda x: x["id"])

    return image_info


def get_stacks_fixed(study_id, case_id, get_cach=False):
    # ---
    if get_cach:
        images = get_studies_from_cach(study_id)
        if images:
            return images
    # ---
    images = get_images_stacks(study_id)
    # ---
    if not images:
        images = get_images(f"https://radiopaedia.org/cases/{case_id}/studies/{study_id}")
    # ---
    if images:
        dump_it(study_id, images)
    # ---
    return images


def main():
    n = 0
    # ---
    # ids_to_work = jsons.all_ids
    ids_to_work = {}
    # ---
    no_id = 0
    # ---
    for url in jsons.urls:
        # ---
        caseid = urls_to_ids.get(url, "")
        # ---
        if caseid and jsons.cases_in_ids.get(caseid):
            continue
        # ---
        no_id += 1 if not caseid else 0
        # ---
        tab = {"url": url, "studies": []}
        if caseid and jsons.all_ids.get(caseid):
            tab.update(jsons.all_ids[caseid])
        # ---
        ids_to_work[url] = tab
    # ---
    print(f"len ids_to_work: {len(ids_to_work)}, no_id: {no_id}")
    # ---
    for _, tab in ids_to_work.items():
        for study in tab["studies"]:
            n += 1
            print(f"n: {n}/ f {len(ids_to_work)}")
            # study id
            # ---
            st_id = study.split("/")[-1]
            # ---
            from_cach = get_studies_from_cach(st_id)
            # ---
            if from_cach:
                continue
            # ---
            # st_file = studies_dir / f"{st_id}.json"
            # if os.path.exists(st_file): continue
            # ---
            ux = get_images_stacks(st_id)
            # ---
            if not ux:
                ux = get_images(study)
            # ---
            if ux:
                dump_it(st_id, ux)


if __name__ == "__main__":
    main()
