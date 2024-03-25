'''

python3 core8/pwb.py mass/radio/st2/start2 nodiff test
python3 core8/pwb.py mass/radio/st2/start2 nodiff get:55

'''
import sys
import psutil
import tqdm
import json
import os
from pathlib import Path
from multiprocessing import Pool
# ---
from newapi import printe
from mass.radio.st2.One_Case import OneCase
# ---
main_dir = Path(__file__).parent.parent
# ---
with open(main_dir / 'jsons/authors.json', 'r', encoding='utf-8') as f:
    authors = json.load(f)
# ---
with open(main_dir / 'jsons/infos.json', 'r', encoding='utf-8') as f:
    infos = json.load(f)
# ---
with open(os.path.join(str(main_dir), 'jsons/all_ids.json'), 'r', encoding='utf-8') as f:
    all_ids = json.load(f)
# ---
# cases_in_ids = []
# ---
with open(main_dir / 'jsons/cases_in_ids.json', 'r', encoding='utf-8') as f:
    cases_in_ids = json.load(f)
# ---
ids_by_caseId = {x: v for x, v in all_ids.items() if x not in cases_in_ids}
# ---
del cases_in_ids
del all_ids


def print_memory():

    _red_ = "\033[91m%s\033[00m"

    usage = psutil.Process(os.getpid()).memory_info().rss
    usage = usage / 1024 // 1024

    print(_red_ % f'memory usage: psutil {usage} MB')


def do_it(va):
    # ---
    case_url = va['case_url']
    caseId = va['caseId']
    title = va['title']
    studies = va['studies']
    author = va['author']
    # ---
    bot = OneCase(case_url, caseId, title, studies, author)
    bot.start()
    # ---
    del bot, author, title, studies


def multi_work(tab):
    done = 0
    pool = Pool(processes=5)
    pool.map(do_it, tab)
    pool.close()
    pool.terminate()
    # ---
    done += len(tab)
    print_memory()
    # ---
    printe.output(f'<<purple>> done: {done}:')


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
            tabs[str(num)] = dict(list(ids_tab.items())[i: i + length])
            # print(f'tab {num} : {len(tabs[str(num)])}')
            print(f'tfj run mu{num} --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st2/start2 nodiff get:{num} {len(tabs[str(num)])}"')

        for arg in sys.argv:
            arg, _, value = arg.partition(':')
            if arg == 'get':
                ids_tab = tabs[value]
                print(f'work in {len(ids_tab)} cases')
        del tabs
    # ---
    tab = []
    # ---
    n = 0
    for _, va in tqdm.tqdm(ids_tab.items()):
        n += 1
        # ---
        caseId = va['caseId']
        case_url = va['url']
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
    del ids_tab
    # ---
    multi_work(tab)


if __name__ == "__main__":
    # ---
    if 'test' in sys.argv:
        ids_by_caseId = {
            "98997": {
                "caseId": 98997,
                "title": "C6-C7 fracture dislocation",
                "studies": [
                    "https://radiopaedia.org/cases/98997/studies/120238"
                ],
                "url": "https://radiopaedia.org/cases/c6-c7-fracture-dislocation",
                "system": "Musculoskeletal",
                "author": "Bahman Rasuli",
                "published": "18 Apr 2022"
            }
        }
    # ---
    print('ids_by_caseId: ', len(ids_by_caseId))
    # ---
    main(ids_by_caseId)
