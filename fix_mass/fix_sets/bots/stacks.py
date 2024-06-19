"""

from fix_mass.fix_sets.bots.stacks import get_stacks# get_stacks(study_id)

"""
import requests
import json
from newapi import printe
from fix_mass.fix_sets.jsons_dirs import get_study_dir


def dump_it(data, study_id):
    # ---
    study_id_dir = get_study_dir(study_id)
    # ---
    file = study_id_dir / "stacks.json"
    # ---
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        printe.output(f"<<green>> write {len(data)} to file: {file}")


def get_stacks_o(study_id):
    new_url = f"https://radiopaedia.org/studies/{study_id}/stacks"
    print(f"get_images_stacks: study_id: {study_id}, new_url: {new_url}")
    # ---
    try:
        response = requests.get(new_url, timeout=10)
    except Exception as e:
        print(f"Failed to retrieve content from the URL. Error: {e}")
        return {}
    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
        return {}

    text = response.text
    if not text.startswith("[") and not text.endswith("]"):
        print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
        return {}

    json_data = json.loads(text)

    return json_data


def get_stacks(study_id):
    # ---
    data = get_stacks_o(study_id)
    # ---
    if data:
        dump_it(data, study_id)
    # ---
    return data
