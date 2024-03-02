"""

python3 core8/pwb.py mass/radio/st3/count
tfj run countca --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/count"
"""
import os
import sys
import json
import tqdm
from pathlib import Path
from mass.radio.studies import get_images_stacks, get_images
from newapi.ncc_page import MainPage as ncc_MainPage

main_dir = Path(__file__).parent.parent

with open(main_dir / "jsons/ids.json", "r", encoding="utf-8") as f:
    ids = json.load(f)

with open(main_dir / "jsons/cases_in_ids.json", "r", encoding="utf-8") as f:
    cases_in_ids = json.load(f)

ids_tab = {x: v for x, v in ids.items() if x not in cases_in_ids}

cases_done = len(ids) - len(ids_tab)

class All:
    cases = 0
    images = 0
    studies = 0
    
All.cases = len(ids_tab)

def get_studies(studies_ids, caseId):
    images_count = 0
    for study in studies_ids:
        st_file = main_dir / "studies" / f"{study}.json"
        images = {}
        if os.path.exists(st_file):
            try:
                with open(st_file, "r", encoding="utf-8") as f:
                    images = json.load(f)
            except Exception as e:
                print(f"{study} : error")
        images = [image for image in images if image]
        if not images:
            images = get_images_stacks(caseId)
        if not images:
            url = f"https://radiopaedia.org/cases/{caseId}/studies/{study}"
            images = get_images(url)
        images_count += len(images)

    return images_count

def sa():
    text = ""
    
    text += f"* All Cases: {len(ids):,}\n"
    text += f"* Cases done: {cases_done:,}\n\n"
    text += f";Remaining:\n"
    text += f"* Cases: {All.cases:,}\n"
    text += f"* Images: {All.images:,}\n"
    text += f"* Studies: {All.studies:,}\n"

    print(text)

    page = ncc_MainPage("User:Mr. Ibrahem/Radiopaedia", 'www', family='nccommons')

    if page.exists():
        page.save(newtext=text, summary='update')
    else:
        page.Create(text=text, summary='update')
    
def start():
    print(f"<<purple>> start.py all: {len(ids_tab)}:")
    n = 0
    for _, va in tqdm.tqdm(ids_tab.items()):
        n += 1
        caseId = va["caseId"]

        studies = [study.split("/")[-1] for study in va["studies"]]
        All.studies += len(studies)

        images = get_studies(studies, caseId)
        All.images += images

        if "test" in sys.argv and n == 100:
            break
    
    sa()

if __name__ == '__main__':
    start()
        
