'''

python3 core8/pwb.py mass/radio/start2 nodiff test
python3 core8/pwb.py mass/radio/start2 nodiff get:55

'''
import re
import sys
import psutil
import time
import json
import os
import pywikibot
from pathlib import Path
# ---
from newapi import printe
from newapi.ncc_page import CatDepth

from multiprocessing import Pool
from mass.radio.One_Case import OneCase

# from mass.radio.jsons_files import jsons#, dumps_jsons, ids_to_urls, urls_to_ids
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, ids=0, all_ids=0, urls_to_get_info=0)

main_dir = Path(__file__).parent
# ---
with open(os.path.join(str(main_dir), 'jsons/authors.json'), 'r', encoding='utf-8') as f:
    authors = json.load(f)
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
ids_by_caseId = { x:v for x,v in ids.items() if not x in cases_in_ids }
# ---

def print_memory():

    _red_ = "\033[91m%s\033[00m"
    _blue_ = "\033[94m%s\033[00m"
    _yellow_ = "\033[93m%s\033[00m"

    usage = psutil.Process(os.getpid()).memory_info().rss
    pywikibot.output(_red_ % f'memory usage: psutil {usage / 1024 / 1024} MB')

def get_pages():
    printe.output('<<purple>> start.py get_pages:')
    # ---
    pages2 = CatDepth('Category:Radiopaedia images by case', sitecode='www', family="nccommons", depth=0, ns="all")
    # ---
    reg = r'^Category:Radiopaedia case (\d+) (.*?)$'
    # ---
    for cat in pages2:
        match = re.match(reg, cat)
        if match:
            cases_in_ids.append(str(match.group(1)))

def do_it(va):
    case_url = va['case_url']
    caseId = va['caseId']
    title = va['title']
    studies = va['studies']
    author = va['author']
    # ---
    bot = OneCase(case_url, caseId, title, studies, author)
    bot.start()
    # ---
    time.sleep(1)
    # ---
    print_memory()


def multi_work(tab):
    pool = Pool(processes=5)
    pool.map(do_it, tab)
    pool.terminate()

def main(ids_tab):
    printe.output(f'<<purple>> start.py all: {len(ids_tab)}:')
    # ---
    print_memory()
    # ---
    if 'test' not in sys.argv:
        tabs = {}
        print(f'all cases: {len(ids_tab)}')
        length = len(ids_tab) // 13
        for i in range(0, len(ids_tab), length):
            num = i//length+1
            tabs[str(num)] = dict(list(ids_tab.items())[i : i + length])
            # print(f'tab {num} : {len(tabs[str(num)])}')
            print(f'tfj run mu{num} --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start2 nodiff get:{num} {len(tabs[str(num)])}"')
        
        for arg in sys.argv:
            arg, _, value = arg.partition(':')
            if arg == 'get':
                ids_tab = tabs[value]
                print(f'work in {len(ids_tab)} cases')
        del tabs
    # ---
    printe.output(f'<<purple>> cases_in_ids: {len(cases_in_ids)}:')
    # ---
    tab = []
    # ---
    n = 0
    for k, va in ids_tab.items():
        n += 1
        # ---
        caseId   = va['caseId']
        case_url = va['url']
        # ---
        if caseId in cases_in_ids or str(caseId) in cases_in_ids:
            printe.output(f'<<purple>> caseId {caseId} already in cases_in_ids')
            continue
        # ---
        author = va.get('author', '')
        # ---
        if not author:
            author = infos.get(case_url, {}).get(str(caseId), '')
        # ---
        if not author:
            author = authors.get(str(caseId), '')
        # ---
        title = va['title']
        # ---
        studies = [study.split('/')[-1] for study in va['studies']]
        # ---
        tab.append({'caseId': caseId, 'case_url': case_url, 'title': title, 'studies': studies, 'author': author})
    # ---
    multi_work(tab)

if __name__ == "__main__":
    # ---
    print('ids_by_caseId: ', len(ids_by_caseId))
    # ---
    if 'test' in sys.argv:
        ids_by_caseId = {
            "20476": {
                "url": "https://radiopaedia.org/cases/peritonsillar-abscess-quinsy",
                "caseId": 20476,
                "title": "Peritonsillar abscess (quinsy)",
                "studies": [
                    "https://radiopaedia.org/cases/20476/studies/20387"
                ],
                "author": "Chris O'Donnell"
            }
        }
    # ---
    main(ids_by_caseId)