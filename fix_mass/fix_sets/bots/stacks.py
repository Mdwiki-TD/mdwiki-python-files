"""

from fix_mass.fix_sets.bots.stacks import get_stacks# get_stacks(study_id)

"""
import requests
import json

def get_stacks(study_id):
    new_url = f"https://radiopaedia.org/studies/{study_id}/stacks"
    print(f"get_images_stacks: study_id: {study_id}, new_url: {new_url}")
    # ---
    response = requests.get(new_url, timeout=10)

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
