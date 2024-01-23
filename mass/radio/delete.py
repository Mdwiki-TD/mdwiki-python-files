#!/usr/bin/python3
"""
python3 core8/pwb.py mass/radio/delete
"""
#
# (C) Ibrahem Qasim, 2023
#
# ---
from nccommons import api
from new_api.ncc_page import CatDepth
# ---
cats = CatDepth('Category:Cats to delete', sitecode='www', family="nccommons", depth=0, ns="all")
# ---
print(f'len of cats: {len(cats)}')
# ---
for cat in cats:
    print(f'cat: {cat}')
    # ---
    members = CatDepth(cat, sitecode='www', family="nccommons", depth=0, ns="all")
    # ---
    if not members:
        params = {"action": "delete", "format": "json", "title": cat, "reason": "empty category"}
        # ---
        xx= api.post_s(params, addtoken=True)
        # ---
        print(xx)
    # break