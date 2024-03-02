'''

python3 core8/pwb.py mass/radio/st3/count
'''
import sys
import os
import json
import tqdm
from pathlib import Path
from mass.radio.studies import get_images_stacks, get_images
# ---
from newapi import printe
# ---
main_dir = Path(__file__).parent.parent
# ---
with open(os.path.join(str(main_dir), 'jsons/ids.json'), 'r', encoding='utf-8') as f:
    ids = json.load(f)
# ---
with open(os.path.join(str(main_dir), 'jsons/cases_in_ids.json'), 'r', encoding='utf-8') as f:
    cases_in_ids = json.load(f)
# ---
ids_tab = { x:v for x,v in ids.items() if x not in cases_in_ids }
# ---
def get_studies(studies_ids, caseId):
    images_count = 0
    for study in studies_ids:
            st_file = os.path.join(str(main_dir), 'studies', f'{study}.json')
            # ---
            images = {}
            # ---
            if os.path.exists(st_file):
                try:
                    with open(st_file, 'r', encoding='utf-8') as f:
                        images = json.loads(f.read())
                except Exception as e:
                    print(f'{study} : error')
            # ---
            images = [ image for image in images if image ]
            # ---
            if not images:
                images = get_images_stacks(caseId)
            # ---
            if not images:
                images = get_images(f'https://radiopaedia.org/cases/{caseId}/studies/{study}')
            # ---
            images_count += len(images)
    return images_count
    
class All:
    pass

All.images = 0
All.studies = 0

printe.output(f'<<purple>> start.py all: {len(ids_tab)}:')
# ---
for _, va in tqdm.tqdm(ids_tab.items()):
    caseId   = va['caseId']
    studies = [study.split('/')[-1] for study in va['studies']]
    # ---
    All.studies += len(studies)
    # ---
    images = get_studies(studies, caseId)
    All.images += images

print(f"{All.images=}")
print(f"{All.studies=}")


