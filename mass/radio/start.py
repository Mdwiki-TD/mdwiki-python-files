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

authors_file = os.path.join(str(main_dir), 'jsons/authors.json')
with open(authors_file, 'r', encoding='utf-8') as f:
    authors = json.loads(f.read())

ids_file = os.path.join(str(main_dir), 'jsons/ids.json')
with open(ids_file, 'r', encoding='utf-8') as f:
    ids = json.loads(f.read())

def get_pages():
        
    pages = CatDepth('Category:Uploads by Mr. Ibrahem', sitecode='www', family="nccommons", depth=0, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])
    pages2 = CatDepth('Category:Radiopaedia images by case', sitecode='www', family="nccommons", depth=0, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])
    pages3 = CatDepth('Category:Radiopaedia sets', sitecode='www', family="nccommons", depth=0, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])

    pages = pages | pages2
    pages = pages | pages3
    return pages

def main(ids_tab):
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

    pages = get_pages()

    for n, (case_url, tab) in enumerate(ids_tab.items(), start=1):
        caseId  = tab['caseId']
        printe.output(f'<<purple>> case:{n} / {len(ids_tab)}:')
        author = authors.get(str(caseId), '')
        title   = tab['title']

        studies = [ study.split('/')[-1] for study in tab['studies'] ]
        bot = OneCase(case_url, caseId, title, studies, pages, author)
        bot.start()
        if n % 100 == 0:
            print(f'processed {n} cases')
            # break

if __name__ == "__main__":
    if 'test' in sys.argv:
        ids = {
            "https://radiopaedia.org/cases/absent-ulnar-styloid-process": {
        "caseId": 53712,
        "title": "Absent ulnar styloid process",
        "studies": [
            "https://radiopaedia.org/cases/53712/studies/59772"
        ]
    }
    }
    #---
    main(ids)
