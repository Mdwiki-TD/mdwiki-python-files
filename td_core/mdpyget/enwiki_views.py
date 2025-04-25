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

if os.getenv("HOME"):
    Dashboard_path = os.getenv("HOME") + "/public_html/td"
else:
    Dashboard_path = "I:/mdwiki/mdwiki/public_html/td"


def make_n_views(old_views, RTT, n_views):
    # ---
    en_keys = [mdwiki_to_enwiki.get(cc, cc) for cc in RTT]
    # ---
    en_keys.append("Cisatracurium")
    # ---
    print(f"start get_views_with rest_v1: length: {len(en_keys)}")
    # ---
    if "newpages" in sys.argv:
        en_keys_2 = list(en_keys)
        en_keys = [xp for xp in en_keys_2 if old_views.get(xp, 0) < 10]
        # ---
        printe.output(f"en_keys:{len(en_keys_2)}, new en_keys:{len(en_keys)}")
    # ---
    en_keys = [re.sub(r"^Video:", "Wikipedia:VideoWiki/", x, flags=re.IGNORECASE) for x in en_keys]
    # ---
    enviews = views_rest.get_views_last_30_days("en", en_keys)
    # ---
    printe.output(f"len of enviews: {len(enviews.keys())}")
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
        n_views[k] = view
    # ---
    printe.output(f"no_views:{no_views},\t len of n_views: {len(n_views.keys())}")
    # ---
    return n_views


def start_to_sql(tab):
    tab = [{"title": x, "en_views": v} for x, v in tab.items()]
    # ---
    to_sql(tab, "enwiki_pageviews", columns=["title", "en_views"], title_column="title")


def main():
    # ---
    old_views = {}
    # ---
    enwiki_pageviews = Dashboard_path + "/Tables/jsons/enwiki_pageviews.json"
    # ---
    with open(enwiki_pageviews, "r", encoding="utf-8-sig") as file:
        old_views = json.load(file)
    # ---
    n_views = dict(old_views.items())
    # ---
    RTT = get_links_from_cats()
    # ---
    n_views = make_n_views(old_views, RTT, n_views)
    # ---
    if "nodump" in sys.argv:
        # ---
        with open(enwiki_pageviews, "w", encoding="utf-8") as outfile:
            json.dump(n_views, outfile, sort_keys=True, indent=2)
    # ---
    start_to_sql(n_views)


if __name__ == "__main__":
    main()
