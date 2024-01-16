'''

python3 core8/pwb.py mass/radio/start nodiff test

'''
import sys
import os
from new_api import printe
from pathlib import Path
import re
import requests
import json

from new_api.ncc_page import CatDepth
from mass.radio.One_Case import OneCase
main_dir = Path(__file__).parent

# ---
authors_file = os.path.join(str(main_dir), 'jsons/authors.json')
with open(authors_file, 'r', encoding='utf-8') as f:
    authors = json.loads(f.read())
# ---
ids_file = os.path.join(str(main_dir), 'jsons/ids.json')
with open(ids_file, 'r', encoding='utf-8') as f:
    ids_by_caseId = json.loads(f.read())
# ---
pages_all = {}
# ---


def get_pages():
    pages = CatDepth('Category:Uploads by Mr. Ibrahem', sitecode='www', family="nccommons", depth=0, ns="all")
    pages2 = CatDepth('Category:Radiopaedia images by case', sitecode='www', family="nccommons", depth=0, ns="all")
    pages3 = CatDepth('Category:Radiopaedia sets', sitecode='www', family="nccommons", depth=0, ns="all")

    pages = pages | pages2
    pages = pages | pages3

    return pages


def main(ids_tab):
    global pages_all
    if 'test' not in sys.argv:
        tabs = {"1": {}, "2": {}, "3": {}, "4": {}}
        print(f'all cases: {len(ids_tab)}')
        length = len(ids_tab) // 4
        for i in range(0, len(ids_tab), length):
            tabs[str(i//length+1)] = dict(list(ids_tab.items())[i:i+length])
            print(f'tab {i//length+1} : {len(tabs[str(i//length+1)])}')

        for arg in sys.argv:
            arg, _, value = arg.partition(':')
            if arg == 'get':
                ids_tab = tabs[value]
                print(f'work in {len(ids_tab)} cases')

    if pages_all == {}:
        pages_all = get_pages()

    n = 0
    for k, tab in ids_tab.items():
        n += 1
        caseId = tab['caseId']
        case_url = tab['url']
        printe.output('++++++++++++++++++++++++++++++++')
        printe.output(f'<<purple>> case:{n} / {len(ids_tab)}:')
        author = authors.get(str(caseId), '')
        title = tab['title']

        studies = [study.split('/')[-1] for study in tab['studies']]
        bot = OneCase(case_url, caseId, title, studies, pages_all, author)
        bot.start()
        if n % 100 == 0:
            print(f'processed {n} cases')
            # break


if __name__ == "__main__":
    if 'test' in sys.argv:
        ids_by_caseId = {
            "42290": {
                "url": "https://radiopaedia.org/cases/active-colonic-bleeding-importance-of-preliminary-non-contrast-arterial-phase-and-delayed-phase-imaging-on-ct-mesenteric-angiography",
                "caseId": 42290,
                "title": "Active colonic bleeding: importance of preliminary non-contrast, arterial phase and delayed phase imaging on CT mesenteric angiography",
                "studies": [
                    "https://radiopaedia.org/cases/42290/studies/45394",
                    "https://radiopaedia.org/cases/42290/studies/45397"
                ]
            }
        }
    # ---
    main(ids_by_caseId)
