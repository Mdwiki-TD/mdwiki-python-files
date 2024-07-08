"""
from wprefs.files import reffixed_list, setting, append_reffixed_file
"""
#
# (C) Ibrahem Qasim, 2023
#
#
import json

import os
import sys
from pathlib import Path

# ---
pathse = [
    "/data/project/mdwiki/pybot/md_core/",
    "/data/project/medwiki/pybot/md_core/",
    "/data/project/mdwiki/pybot/",
    "/data/project/medwiki/pybot/",
]
# ---
for path in pathse:
    sys.path.append(path)
# ---
from wprefs.helps import exepts

Dir = str(Path(__file__).parents[0])
dir2 = Dir.replace("\\", "/").split("/pybot/")[0]
# ---
fixwikirefs = dir2 + '/confs/fixwikirefs.json'
reffixed_file = f'{Dir}/reffixed.csv'
# ---
setting = {}
# ---
if os.path.isfile(fixwikirefs):
    try:
        setting = json.load(open(fixwikirefs, "r", encoding="utf-8-sig"))
        # print(setting)
    except Exception:
        setting = {}


def make_ref_done_list():
    # ---
    reffixed = ''
    # ---
    try:
        with open(reffixed_file, "r", encoding="utf-8-sig") as mama:
            reffixed = mama.read()
    except Exception:
        exepts()
    # ---
    reffixed_list = [x.strip() for x in reffixed.split('\n') if x.strip() != '']
    # ---
    return reffixed_list


reffixed_list = make_ref_done_list()


def append_reffixed_file(lang, title, titles=[]):
    lio = f'{lang}:{title}'
    # ---
    if titles:
        nan = "\n".join([f'{lang}:{t}' for t in titles])
        lio += f"\n{nan}"
    # ---
    with open(reffixed_file, "a", encoding="utf-8") as ggg:
        ggg.write('\n' + lio)


def save_wprefcash(title, newtext):
    # ---
    title2 = title
    title2 = title2.replace(':', '-').replace('/', '-').replace(' ', '_')
    # ---
    try:
        filename = dir2 + '/public_html/wprefcash/' + title2 + '.txt'
        with open(filename, "w", encoding="utf-8") as uy:
            uy.write(newtext)
        # ---
        print(filename)
        # ---
    except Exception:
        exepts()

        filename = dir2 + '/public_html/wprefcash/title2.txt'
        with open(filename, "w", encoding="utf-8") as gf:
            gf.write(newtext)
        # ---
        print(filename)
    # ---
    return ''
