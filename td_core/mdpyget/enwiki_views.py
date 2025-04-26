#!/usr/bin/python3
"""

إنشاء قائمة بمشاهدات المقالات من الانجليزية

وحفظها في Dashboard_path
+
قاعدة البيانات

python3 core8/pwb.py mdpyget/enwiki_views newpages nodump
python3 core8/pwb.py mdpyget/enwiki_views newpages

"""
import re
import os
import sys
import json

from apis import views_rest
from newapi import printe
from mdpy.bots.en_to_md import enwiki_to_mdwiki, mdwiki_to_enwiki
from mdpyget.pages_list import get_links_from_cats
from mdpyget.bots.to_sql import to_sql
from mdapi_sql import sql_for_mdwiki

if os.getenv("HOME"):
    Dashboard_path = os.getenv("HOME") + "/public_html/td"
else:
    Dashboard_path = "I:/mdwiki/mdwiki/public_html/td"
# ---
data_tab = {1: {}}


def make_n_views(en_keys, old_values):
    # ---
    en_keys = [re.sub(r"^Video:", "Wikipedia:VideoWiki/", x, flags=re.IGNORECASE) for x in en_keys]
    # ---
    enviews = views_rest.get_views_last_30_days("en", en_keys)
    # ---
    enviews_0 = {k: v for k, v in enviews.items() if v == 0}
    # ---
    printe.output(f"<<purple>> len of enviews: {len(enviews.keys())}, len of enviews_0: {len(enviews_0.keys())}")
    # ---
    no_views = 0
    # ---
    for k, view in enviews.items():
        if view == 0:
            no_views += 1
            continue
        # ---
        k = k.replace("Wikipedia:VideoWiki/", "Video:")
        # ---
        if enwiki_to_mdwiki.get(k):
            k = enwiki_to_mdwiki.get(k)
        # ---
        old_values[k] = view
    # ---
    printe.output(f"no_views:{no_views},\t len of old_values: {len(old_values.keys())}")
    # ---
    return old_values


def start_to_sql(tab):
    tab = [{"title": x, "en_views": v} for x, v in tab.items()]
    # ---
    to_sql(tab, "enwiki_pageviews", columns=["title", "en_views"], title_column="title")


def get_old_values(json_file):
    # ---
    old_values = {}
    # ---
    with open(json_file, "r", encoding="utf-8-sig") as file:
        old_values = json.load(file)
    # ---
    que = "select DISTINCT title, en_views from enwiki_pageviews"
    # ---
    in_sql = sql_for_mdwiki.mdwiki_sql_dict(que)
    # ---
    old_values.update({x["title"]: x["en_views"] for x in in_sql if x["en_views"] > 0 and x["title"] not in old_values})
    # ---
    return old_values


def main():
    # ---
    printe.output("Get vaild_links from cat : RTT")
    # ---
    cat_get = "Videowiki scripts" if "video" in sys.argv else ""
    # ---
    vaild_links = get_links_from_cats(cat_get)
    # ---
    printe.output(f"len of vaild_links: {len(vaild_links)}")
    # ---
    json_file = f"{Dashboard_path}/Tables/jsons/enwiki_pageviews.json"
    # ---
    old_values = get_old_values(json_file)
    # ---
    len_old = len(old_values)
    # ---
    data_tab[1] = dict(old_values.items())
    # ---
    vaild_links = [mdwiki_to_enwiki.get(cc, cc) for cc in vaild_links]
    # ---
    if "newpages" in sys.argv:
        en_keys_2 = list(vaild_links)
        vaild_links = [xp for xp in en_keys_2 if old_values.get(xp, 0) < 10]
        # ---
        printe.output(f"vaild_links:{len(en_keys_2)}, new vaild_links:{len(vaild_links)}")
    # ---
    if "video" in sys.argv:
        vaild_links = [x for x in vaild_links if x.startswith("Video:")]
    # ---
    data_tab[1] = make_n_views(vaild_links, data_tab[1])
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
