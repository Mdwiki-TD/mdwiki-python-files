#!/usr/bin/python3
"""

إنشاء قائمة بالاهمية من الانجليزية

python3 core8/pwb.py mdpyget/getas newpages

"""
import re
import os
import json
import sys
from mdpy.bots.en_to_md import enwiki_to_mdwiki
from newapi import printe
from newapi.wiki_page import NEW_API
from mdpyget.pages_list import get_links_from_cats
from mdpyget.bots.to_sql import to_sql

api_new = NEW_API("en", family="wikipedia")

# ---
fals_ase = ["", "na", "unknown"]
# ---
if os.getenv("HOME"):
    Dashboard_path = os.getenv("HOME") + "/public_html/td"
else:
    Dashboard_path = "I:/mdwiki/mdwiki/public_html/td"
# ---
assessments_tab = {1: {}}
# ---
json_file = {0: f"{Dashboard_path}/Tables/jsons/assessments.json"}
Nore = {1: False}
# ---
for arg in sys.argv:
    if arg in ["new", "listnew", "less100", "more400"]:
        Nore[1] = True


def log(len_old):
    with open(json_file[0], "w", encoding="utf-8") as outfile:
        json.dump(assessments_tab[1], outfile, sort_keys=True)
    # ---
    printe.output(f"<<green>> {len(assessments_tab[1])} lines to {json_file[0]}")
    printe.output(f"<<green>> len old assessments {len_old}")


def work_for_list(listn):
    # ---
    # من ميد إلى الإنجليزية
    # listo = [mdwiki_to_enwiki.get(cc, cc) for cc in listn]
    # ---
    listn = [re.sub(r"^Video:", "Wikipedia:VideoWiki/", x, flags=re.IGNORECASE) for x in listn]
    # ---
    result = api_new.get_pageassessments("|".join(listn))
    # ---
    ase = {x["title"]: x for x in result}
    # ---
    lenn = 0
    # ---
    for title, tabe in ase.items():
        # ---
        # {'pageid': 3186837, 'ns': 0, 'title': 'WAGR syndrome', 'pageassessments': {'Medicine': {'class': 'Start', 'importance': 'Low'}}}
        # ---
        importance = tabe.get("pageassessments", {}).get("Medicine", {}).get("importance", "")
        # ---
        if importance.lower() in fals_ase and title.startswith("Wikipedia:VideoWiki/"):
            importance = tabe.get("pageassessments", {}).get("Videowiki", {}).get("importance", "")
        # ---
        if "video" in sys.argv:
            printe.output(f"{title} : {importance}")
        # ---
        title = title.replace("Wikipedia:VideoWiki/", "Video:")
        # ---
        # من الإنجليزية إلى ميد
        title = enwiki_to_mdwiki.get(title, title)
        # ---
        lenn += 1
        # ---
        assessments_tab[1][title] = importance
    # ---
    printe.output(f"len of new assessments:{lenn}")


def mmain():
    # ---
    printe.output("Get vaild_links from cat : RTT")
    # ---
    cat_get = "Videowiki scripts" if "video" in sys.argv else ""
    # ---
    vaild_links = get_links_from_cats(cat_get)
    # ---
    printe.output(f"len of vaild_links: {len(vaild_links)}")
    # ---
    lala = ""
    # ---
    with open(json_file[0], "r", encoding="utf-8-sig") as listt:
        lala = listt.read()
    # ---
    printe.output(f"file_name:{json_file[0]}")
    fa = str(lala)
    old_assess = json.loads(fa) if fa != "" else {}
    # ---
    len_old = len(old_assess)
    # ---
    assessments_tab[1] = dict(old_assess.items())
    # ---
    if "newpages" in sys.argv:  # vaild_links
        vaild_links2 = vaild_links
        vaild_links = [xp for xp in vaild_links2 if (xp not in old_assess or old_assess.get(xp, "").lower() in fals_ase)]
        # ---
        printe.output(f"Category-members:{len(vaild_links2)}, New-members:{len(vaild_links)}")
    # ---
    if "video" in sys.argv:
        vaild_links = [x for x in vaild_links if x.startswith("Video:")]
    # ---
    vaild_links.sort()
    # ---
    kkk = {1: vaild_links}
    # ---
    if "new" not in sys.argv:
        kkk[1] = []
        for x in vaild_links:
            x2 = x[0].upper() + x[1:]
            kkk[1].append(x2)
    # ---
    for i in range(0, len(kkk[1]), 50):
        group = kkk[1][i : i + 50]
        work_for_list(group)
    # ---
    log(len_old)
    # ---
    start_to_sql(assessments_tab[1])


def start_to_sql(tab):
    tab = [{"title": x, "importance": v} for x, v in tab.items()]
    # ---
    to_sql(tab, "assessments", columns=["title", "importance"], title_column="title")


def test():
    # python3 core8/pwb.py mdpyget/getas test
    # ---
    assessments_tab[1]["Yemen1"] = "Top"
    # ---
    assessments_tab[1]["Sana'a"] = "Mid"
    assessments_tab[1]["Sanax"] = "Mid"
    # ---
    start_to_sql(assessments_tab[1])


if __name__ == "__main__":
    if "test" in sys.argv:
        test()
    else:
        mmain()
