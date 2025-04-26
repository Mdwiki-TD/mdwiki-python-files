#!/usr/bin/python3
"""

إنشاء قائمة بالاهمية من الانجليزية

وحفظها في Dashboard_path
+
قاعدة البيانات

python3 core8/pwb.py mdpyget/getas from_cats newpages nowork
python3 core8/pwb.py mdpyget/getas newpages nowork
python3 core8/pwb.py mdpyget/getas video

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
from mdapi_sql import sql_for_mdwiki

api_new = NEW_API("en", family="wikipedia")

# ---
fals_ase = ["", "na", "unknown"]
# ---
if os.getenv("HOME"):
    Dashboard_path = os.getenv("HOME") + "/public_html/td"
else:
    Dashboard_path = "I:/mdwiki/mdwiki/public_html/td"
# ---
data_tab = {1: {}}


def work_for_list(en_keys, old_values):
    # ---
    # من ميد إلى الإنجليزية
    # listo = [mdwiki_to_enwiki.get(cc, cc) for cc in en_keys]
    # ---
    en_keys = [re.sub(r"^Video:", "Wikipedia:VideoWiki/", x, flags=re.IGNORECASE) for x in en_keys]
    # ---
    lenn = 0
    # ---
    for i in range(0, len(en_keys), 50):
        group = en_keys[i : i + 50]
        # ---
        printe.output(f"get_pageassessments: len of group: {len(group)}")
        # ---
        result = api_new.get_pageassessments("|".join(group))
        # ---
        ase = {x["title"]: x for x in result}
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
            lenn += 1 if importance else 0
            # ---
            # data_tab[1][title] = importance
            old_values[title] = importance
    # ---
    printe.output(f"len of new assessments:{lenn}")
    # ---
    return old_values


def start_to_sql(tab):
    tab = [{"title": x, "importance": v} for x, v in tab.items()]
    # ---
    to_sql(tab, "assessments", columns=["title", "importance"], title_column="title")


def get_old_values(json_file):
    # ---
    que = "select DISTINCT title, importance from assessments"
    # ---
    in_sql = sql_for_mdwiki.mdwiki_sql_dict(que)
    # ---
    old_values = {x["title"]: x["importance"] for x in in_sql}
    # ---
    with open(json_file, "r", encoding="utf-8-sig") as file:
        in_json = json.load(file)
        old_values.update({x: y for x, y in in_json.items() if y and x not in old_values})
    # ---
    old_dict = {}
    # ---
    for x, y in old_values.items():
        # ---
        old_dict.setdefault(y, 0)
        # ---
        old_dict[y] += 1
    # ---
    # sort the dictionary by value
    old_dict = dict(sorted(old_dict.items(), key=lambda item: item[1], reverse=True))
    # ---
    for k, v in old_dict.items():
        # ---
        printe.output(f"<<green>> importance:({k}) count:({v})")
    # ---
    return old_values


def main():
    # ---
    printe.output("Get vaild_links from cat : RTT")
    # ---
    cat_get = "Videowiki scripts" if "video" in sys.argv else ""
    # ---
    json_file = f"{Dashboard_path}/Tables/jsons/assessments.json"
    # ---
    old_values = get_old_values(json_file)
    vaild_links = list(old_values.keys())
    # ---
    if "from_cats" in sys.argv:
        vaild_links = get_links_from_cats(cat_get)
    # ---
    printe.output(f"len of vaild_links: {len(vaild_links)}")
    # ---
    len_old = len(old_values)
    # ---
    data_tab[1] = dict(old_values.items())
    # ---
    # vaild_links = [mdwiki_to_enwiki.get(cc, cc) for cc in vaild_links]
    # ---
    en_keys_2 = list(vaild_links)
    # ---
    if "newpages" in sys.argv:
        # ---
        pages_new = [x for x in en_keys_2 if x not in old_values]
        # ---
        pages_fals_ase = [x for x in en_keys_2 if old_values.get(x, "").lower() in fals_ase]
        # ---
        vaild_links = pages_fals_ase + pages_new
        # ---
        printe.output(f"pages_new:{len(pages_new)}, pages_fals_ase:{len(pages_fals_ase)}")
    # ---
    if "video" in sys.argv:
        vaild_links = [x for x in vaild_links if x.startswith("Video:")]
    # ---
    printe.output(f"old vaild_links: {len(en_keys_2)}, new vaild_links: {len(vaild_links)}")
    # ---
    if "nowork" in sys.argv:
        return
    # ---
    data_tab[1] = work_for_list(vaild_links, old_values)
    # ---
    if "nodump" in sys.argv:
        # ---
        with open(json_file, "w", encoding="utf-8") as outfile:
            json.dump(data_tab[1], outfile, sort_keys=True, indent=2)
    # ---
    printe.output(f"<<green>> {len(data_tab[1])} lines to {json_file}")
    printe.output(f"<<green>> len old assessments {len_old}")
    # ---
    start_to_sql(data_tab[1])


def test():
    # python3 core8/pwb.py mdpyget/getas test
    # ---
    data_tab[1]["Yemen1"] = "Top"
    # ---
    data_tab[1]["Sana'a"] = "Mid"
    data_tab[1]["Sanax"] = "Mid"
    # ---
    start_to_sql(data_tab[1])


if __name__ == "__main__":
    if "test" in sys.argv:
        test()
    else:
        main()
