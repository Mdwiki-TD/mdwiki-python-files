"""
import logging
logger = logging.getLogger(__name__)

from wprefs.files import reffixed_list, setting, append_reffixed_file
"""

import json
import os
from pathlib import Path

from wprefs.helps import exepts

Dir = Path(__file__).parents[0]
dir2 = os.getenv("HOME")
# ---
if not dir2:
    dir2 = "I:/mdwiki/mdwiki"
# ---
public_html_dir = dir2 + "/public_html"
# ---
fixwikirefs = dir2 + "/confs/fixwikirefs.json"
reffixed_file = Dir / "reffixed.csv"
# ---
setting = {}
# ---
if os.path.isfile(fixwikirefs):
    try:
        setting = json.load(open(fixwikirefs, "r", encoding="utf-8-sig"))
        # logger.info(setting)
    except Exception:
        setting = {}


def make_ref_done_list():
    # ---
    reffixed = ""
    # ---
    try:
        with open(reffixed_file, "r", encoding="utf-8-sig") as mama:
            reffixed = mama.read()
    except Exception:
        exepts()
    # ---
    reffixed_list = [x.strip() for x in reffixed.split("\n") if x.strip() != ""]
    # ---
    return reffixed_list


reffixed_list = make_ref_done_list()


def append_reffixed_file(lang, title, titles=None):
    if titles is None:
        titles = []
    lio = f"{lang}:{title}"
    # ---
    if titles:
        nan = "\n".join([f"{lang}:{t}" for t in titles])
        lio += f"\n{nan}"
    # ---
    with open(reffixed_file, "a", encoding="utf-8") as ggg:
        ggg.write("\n" + lio)


def save_wprefcash(title, newtext):
    # ---
    title2 = title
    title2 = title2.replace(":", "-").replace("/", "-").replace(" ", "_").replace("'", "_").replace('"', "_")
    # ---
    filename = ""
    # ---
    try:
        filename = public_html_dir + "/wprefcash/" + title2 + ".txt"
        with open(filename, "w", encoding="utf-8") as uy:
            uy.write(newtext)
    except Exception:
        exepts()
        # ---
        filename = public_html_dir + "/wprefcash/title2.txt"
        with open(filename, "w", encoding="utf-8") as gf:
            gf.write(newtext)
    # ---
    return filename
