'''

python3 core8/pwb.py mass/radio/st3/count
'''
import sys
import psutil
import tqdm
import json
import os
from pathlib import Path
# ---
from newapi import printe
from mass.radio.st3.One_Case_New import OneCase
# ---
main_dir = Path(__file__).parent.parent
# ---
with open(os.path.join(str(main_dir), 'jsons/infos.json'), 'r', encoding='utf-8') as f:
    infos = json.load(f)
# ---
with open(os.path.join(str(main_dir), 'jsons/ids.json'), 'r', encoding='utf-8') as f:
    ids = json.load(f)
# ---
# cases_in_ids = []
# ---
with open(os.path.join(str(main_dir), 'jsons/cases_in_ids.json'), 'r', encoding='utf-8') as f:
    cases_in_ids = json.load(f)
# ---
ids_by_caseId = { x:v for x,v in ids.items() if x not in cases_in_ids }
# ---
def do_it(va):
    # ---
    case_url = va['case_url']
    caseId   = va['caseId']
    title        = va['title']
    studies  = va['studies']
    author   = va['author']
    # ---
    bot = OneCase(case_url, caseId, title, studies, author)
    bot.start()

def main(ids_tab):
    printe.output(f'<<purple>> start.py all: {len(ids_tab)}:')
    # ---
    print_memory()
    # ---
    tab = []
    # ---
    n = 0
    for _, va in tqdm.tqdm(ids_tab.items()):
        n += 1
        # ---
        caseId   = va['caseId']
        case_url = va['url']
        # ---
        title = va['title']
        # ---
        studies = [study.split('/')[-1] for study in va['studies']]
        # ---
        tab.append({'caseId': caseId, 'case_url': case_url, 'title': title, 'studies': studies, 'author': ''})
    for x in tab:
        do_it(x)
