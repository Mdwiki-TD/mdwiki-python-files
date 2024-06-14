#!/usr/bin/python3
"""

إنشاء قائمة بالاهمية من الانجليزية

python3 core8/pwb.py /data/project/mdwiki/mdpyget/getas

python3 core8/pwb.py mdpyget/getas newpages

"""

#
# (C) Ibrahem Qasim, 2022
#
#
import json

import os
import sys

# ---
from mdpy.bots.en_to_md import enwiki_to_mdwiki
from mdpy.bots import wiki_api
from mdpy.bots import catdepth2
from mdpy import printe

# ---
# ---
from pathlib import Path

Dir = str(Path(__file__).parents[0])
# print(f'Dir : {Dir}')
# ---
dir2 = Dir.replace("\\", "/")
dir2 = dir2.split("/mdwiki/")[0] + "/mdwiki"
# ---
printe.output("Get vaild_links from cat : RTT")
# ---
tabe = catdepth2.subcatquery2("RTT", depth="2", ns="0")
vaild_links = tabe["list"]
# ---
printe.output(f"len of vaild_links: {len(vaild_links)}")
# ---
json_file = {0: f"{dir2}/public_html/Translation_Dashboard/Tables/assessments.json"}
lala = ""
# ---
with open(json_file[0], "r", encoding="utf-8-sig") as listt:
    lala = listt.read()
# ---
printe.output(f"file_name:{json_file[0]}")
fa = str(lala)
old_assessments = json.loads(fa) if fa != "" else {}
# ---
len_old = len(old_assessments)
# ---
assessments = dict(old_assessments.items())
# ---
if "newpages" in sys.argv:  # vaild_links
    vaild_links2 = vaild_links
    vaild_links = [xp for xp in vaild_links2 if (xp not in old_assessments or old_assessments.get(xp) in ["Unknown", ""])]
    # ---
    printe.output(f"Category-members:{len(vaild_links2)},New-members:{len(vaild_links)}")
    # ---
# ---
Nore = {1: False}
# ---
for arg in sys.argv:
    if arg in ["new", "listnew", "less100", "more400"]:
        Nore[1] = True


def log():
    with open(json_file[0], "w", encoding="utf-8") as outfile:
        json.dump(assessments, outfile, sort_keys=True)
    # ---
    printe.output(f"<<lightgreen>> {len(assessments)} lines to {json_file[0]}")
    printe.output(f"<<lightgreen>> len old assessments {len_old}")


def work_for_list(listn):
    # ---
    # من ميد إلى الإنجليزية
    # listo = [mdwiki_to_enwiki.get(cc, cc) for cc in listn]
    # ---
    ase = wiki_api.Getpageassessments_from_wikipedia("|".join(listn), site="en")
    # ---
    lenn = 0
    # ---
    for title, tabe in ase.items():
        # ---
        # {'pageid': 3186837, 'ns': 0, 'title': 'WAGR syndrome', 'pageassessments': {'Medicine': {'class': 'Start', 'importance': 'Low'}}}
        # ---
        importance = tabe.get("pageassessments", {}).get("Medicine", {}).get("importance", "")
        # ---
        # من الإنجليزية إلى ميد
        title = enwiki_to_mdwiki.get(title, title)
        # ---
        lenn += 1
        # ---
        assessments[title] = importance
    # ---
    printe.output(f"len of new assessments:{lenn}")


def mmain():
    numb = 0
    # ---
    kkk = {1: vaild_links}
    # ---
    if "new" not in sys.argv:
        # kkk = [ x for x in vaild_links if not x in old_assessments ]
        kkk[1] = []
        for x in vaild_links:
            x2 = x[0].upper() + x[1:]
            # if not x in old_assessments or 'listnew' in sys.argv:
            kkk[1].append(x2)
    # ---
    for i in range(0, len(kkk[1]), 50):
        group = kkk[1][i : i + 50]
        work_for_list(group)
        # ---
        # log()
        # ---
    # ---
    log()

    # ---


# ---
if __name__ == "__main__":
    mmain()
# ---
