'''

python3 core8/pwb.py mass/radio/st3/count
'''
import sys
import tqdm
import json
import os
from pathlib import Path
# ---
from newapi import printe
from mass.radio.st3.count_case import OneCase
# ---
main_dir = Path(__file__).parent.parent
# ---
with open(os.path.join(str(main_dir), 'jsons/ids.json'), 'r', encoding='utf-8') as f:
    ids = json.load(f)
# ---
with open(os.path.join(str(main_dir), 'jsons/cases_in_ids.json'), 'r', encoding='utf-8') as f:
    cases_in_ids = json.load(f)
# ---
ids_by_caseId = { x:v for x,v in ids.items() if x not in cases_in_ids }
# ---
class All:
    pass

All.images = 0
All.studies = 0

def do_it(caseId, studies):
    All.studies += len(studies)
    # ---
    bot = OneCase(caseId, studies)
    images = bot.images()
    All.images += images

def main(ids_tab):
    printe.output(f'<<purple>> start.py all: {len(ids_tab)}:')
    # ---
    tab = []
    # ---
    n = 0
    for _, va in tqdm.tqdm(ids_tab.items()):
        n += 1
        # ---
        caseId   = va['caseId']
        studies = [study.split('/')[-1] for study in va['studies']]
        # ---
        do_it(caseId, studies)
    # ---
    print(f"{All.images=}")
    print(f"{All.studies=}")
