"""

python3 core8/pwb.py mass/radio/st3/start3 get:500
python3 core8/pwb.py mass/radio/st3/start3 test nomulti
python3 /data/project/mdwiki/pybot/mass/radio/st3/start3.py test

tfj run mnx1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/start3 get:1 157"
tfj run mnx2 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/start3 get:2 157"
tfj run mnx3 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/start3 get:3 157"
tfj run mnx4 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/start3 get:4 157"
tfj run gnr5 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/start3 get:5 mdwiki"
tfj run gnr6 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/start3 get:6 mdwiki"

"""

import json
import os
import sys
from multiprocessing import Pool
from pathlib import Path

import psutil
import tqdm

# ---
from newapi import printe

from mass.radio.st3.One_Case_New import OneCase

# ---
main_dir = Path(__file__).parent.parent
# ---
with open(main_dir / "jsons/authors.json", encoding="utf-8") as f:
    authors = json.load(f)
# ---
with open(main_dir / "jsons/infos.json", encoding="utf-8") as f:
    infos = json.load(f)
# ---
with open(main_dir / "jsons/all_ids.json", encoding="utf-8") as f:
    all_ids = json.load(f)
# ---
# cases_in_ids = []
# ---
with open(main_dir / "jsons/cases_in_ids.json", encoding="utf-8") as f:
    cases_in_ids = json.load(f)
# ---
ids_by_caseId = {x: v for x, v in all_ids.items() if x not in cases_in_ids}
# ---
del cases_in_ids


def print_memory():
    _red_ = "\033[91m%s\033[00m"

    usage = psutil.Process(os.getpid()).memory_info().rss
    usage = usage / 1024 // 1024

    print(_red_ % f"memory usage: psutil {usage} MB")


def do_it(va):
    # ---
    case_url = va["case_url"]
    caseId = va["caseId"]
    title = va["title"]
    studies = va["studies"]
    author = va["author"]
    # ---
    bot = OneCase(case_url, caseId, title, studies, author)
    bot.start()
    # ---
    del bot, author, title, studies


def multi_work(tab, numb=10):
    done = 0
    for i in range(0, len(tab), numb):
        group = tab[i : i + numb]
        # ---
        done += numb
        printe.output(f"<<purple>> done: {done}:")
        # ---
        print_memory()
        # ---
        if "nomulti" in sys.argv or len(tab) < 10:
            for x in group:
                do_it(x)
        else:
            pool = Pool(processes=5)
            pool.map(do_it, group)
            pool.close()
            pool.terminate()


def ddo(taba):
    ids_tabs = taba
    tabs = {}
    print(f"all cases: {len(ids_tabs)}")
    length = (len(ids_tabs) // 6) + 1
    for i in range(0, len(ids_tabs), length):
        num = i // length + 1
        tabs[str(num)] = dict(list(ids_tabs.items())[i : i + length])
        # print(f'tab {num} : {len(tabs[str(num)])}')
        print(f'tfj run mnx{num} --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/start3 get:{num} {len(tabs[str(num)])}"')

    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg == "get":
            ids_tabs = tabs[value]
            print(f"work in {len(ids_tabs)} cases")
    del tabs

    return ids_tabs


def main(ids_tab):
    printe.output(f"<<purple>> start.py all: {len(ids_tab)}:")
    # ---
    print_memory()
    # ---
    if "test" not in sys.argv and len(ids_tab) > 100:
        ids_tab = ddo(ids_tab)
    # ---
    tab = []
    # ---
    n = 0
    for _, va in tqdm.tqdm(ids_tab.items()):
        n += 1
        # ---
        caseId = va["caseId"]
        case_url = va["url"]
        # ---
        author = va.get("author", "")
        # ---
        if not author:
            author = infos.get(case_url, {}).get(str(caseId), "")
        # ---
        if not author:
            author = authors.get(str(caseId), "")
        # ---
        title = va["title"]
        # ---
        studies = [study.split("/")[-1] for study in va["studies"]]
        # ---
        tab.append(
            {
                "caseId": caseId,
                "case_url": case_url,
                "title": title,
                "studies": studies,
                "author": author,
            }
        )
    # ---
    del ids_tab
    # ---
    multi_work(tab)


def main_by_ids(ids):
    printe.output(f"<<purple>> start.py main_by_ids: {len(ids)=}:")
    # ---
    ids_tab = {caseId: all_ids[caseId] for caseId in ids if caseId in all_ids}
    # ---
    not_in = [c for c in ids if c not in all_ids]
    # ---
    print(f"main_by_ids caseId not in all_ids: {len(not_in)}")
    # ---
    main(ids_tab)


if __name__ == "__main__":
    # ---
    if "test" in sys.argv:
        ids_by_caseId = {
            "161846": {
                "url": "https://radiopaedia.org/cases/cholangiocarcinoma-25",
                "caseId": 161846,
                "title": "Cholangiocarcinoma",
                "studies": ["https://radiopaedia.org/cases/161846/studies/132257"],
                "author": "Mohammadtaghi Niknejad",
                "system": "Hepatobiliary",
                "published": "19 Feb 2023",
            }
        }
    # ---
    print("ids_by_caseId: ", len(ids_by_caseId))
    # ---
    main(ids_by_caseId)
