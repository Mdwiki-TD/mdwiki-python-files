#!/usr/bin/python3
"""

page views bot

python3 core8/pwb.py mdpyget/enwiki_views

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import os
import sys
import json
from pathlib import Path

from apis import views_rest
from newapi import printe
from mdpy.bots.en_to_md import enwiki_to_mdwiki, mdwiki_to_enwiki
from apis import cat_cach

if os.getenv("HOME"):
    Dashboard_path = os.getenv("HOME") + "/public_html/td"
else:
    Dashboard_path = "I:/mdwiki/mdwiki/public_html/td"


def main():
    # ---
    RTT = cat_cach.Cat_Depth("Category:RTT", depth=2, ns="all")
    # ---
    en_keys = [mdwiki_to_enwiki.get(cc, cc) for cc in RTT]
    # ---
    en_keys.append("Cisatracurium")
    # ---
    print(f"start get_views_with rest_v1: length: {len(en_keys)}")
    # ---
    enviews = views_rest.get_views_last_30_days("en", en_keys)
    # ---
    printe.output(f"len of enviews: {len(enviews.keys())}")
    # ---
    no_views = 0
    # ---
    enwiki_pageviews = Dashboard_path + "/Tables/jsons/enwiki_pageviews.json"
    # ---
    old_views = {}
    # ---
    with open(enwiki_pageviews, "r", encoding="utf-8-sig") as file:
        old_views = json.load(file)
    # ---
    n_views = dict(old_views.items())
    # ---
    for k, view in enviews.items():
        if view == 0:
            no_views += 1
            continue
        # ---
        if enwiki_to_mdwiki.get(k):
            k = enwiki_to_mdwiki.get(k)
        # ---
        n_views[k] = view
    # ---
    printe.output(f"no_views:{no_views},\t len of n_views: {len(n_views.keys())}")
    # ---
    if "nodump" not in sys.argv:
        with open(enwiki_pageviews, "w", encoding="utf-8") as outfile:
            json.dump(n_views, outfile, sort_keys=True, indent=2)


if __name__ == "__main__":
    main()
