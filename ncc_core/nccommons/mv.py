#!/usr/bin/python3
"""
python3 core8/pwb.py nccommons/mv
"""
#
# (C) Ibrahem Qasim, 2023
#
# ---
import sys
import json
import os
import codecs

# ---
from newapi import printe
from newapi.ncc_page import MainPage as ncc_MainPage
from newapi.mdwiki_page import NEW_API
from nccommons import api
from mdpy.bots import mdwiki_api

# ---
from pathlib import Path

Dir = str(Path(__file__).parents[0])
# print(f'Dir : {Dir}')
# ---
cats = json.load(open(f'{Dir}/mv.json', 'r', encoding='utf-8'))
# ---
printe.output(f'len of cats: {len(cats)}')
# ---
# ---
api_new = NEW_API('www', family='mdwiki')
api_new.Login_to_wiki()
# pages   = api_new.Find_pages_exists_or_not(liste)
# ---
exists = {}
# exists = api_new.Find_pages_exists_or_not(cats)
# ---
to_create = [x for x, t in exists.items() if t is False]
# ---
printe.output(f'len of to_create: {len(to_create)}')
# ---
n = 0
# ---
for cat in to_create:
    n += 1
    printe.output(f'cat: {n}/{len(to_create)}:')
    text = mdwiki_api.GetPageText(cat)
    new = api.create_Page(text, cat, summary='Copy categories from mdwiki')
# ---
to_update = [x for x, t in exists.items() if t is True]
to_update = cats
# ---
# ---
n = 0


def delete_it(cat):
    # ---
    printe.output(f'cat: {n}/{len(to_update)}:')
    # ---
    params = {"action": "delete", "format": "json", "title": cat, "reason": "cat moved to nccommons.org"}  # , "deletetalk": 1}
    # ---
    doit = mdwiki_api.post_s(params, addtoken=True)
    # ---
    printe.output(f'doit: {doit}')


# ---
for cat in to_update:
    # ---
    n += 1
    # ---
    printe.output(f'cat: {n}/{len(to_update)}:')
    # ---
    nspage = ncc_MainPage(cat, 'www', family='nccommons')
    # ---
    printe.output(f'GetPageText for page:{cat}')
    # ---
    md_text = mdwiki_api.GetPageText(cat)
    # ---
    if md_text == '':
        continue
    # ---
    nc_text = nspage.get_text()
    # ---
    if md_text == nc_text:
        printe.output(f'{cat} is up to date')
    else:
        save_page = nspage.save(newtext=md_text, summary='Copy from mdwiki', nocreate=1)
    # ---
    delete_it(cat)
    # ---
    if 'break' in sys.argv:
        break
    # ---
