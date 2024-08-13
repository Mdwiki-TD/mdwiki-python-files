"""

"""
import json
import os
import stat
from datetime import datetime
from pathlib import Path

from apis import cat_cach
from newapi import printe
from mdpy.bots.check_title import valid_title

Dir = Path(__file__).parent


def from_cach(filename):
    # ---
    if not filename.exists():
        filename.touch(mode=stat.S_IRWXU | stat.S_IRWXG)
        filename.write_text("[]")
    # ---
    # Get the time of last modification
    last_modified_time = os.path.getmtime(filename)
    # ---
    date = datetime.fromtimestamp(last_modified_time).strftime("%Y-%m-%d")
    # ---
    today = datetime.today().strftime("%Y-%m-%d")
    # ---
    if date != today:
        printe.output(f"<<purple>> last modified: {date}, today: {today}. ")
        return {}
    # ---
    with open(filename, "r", encoding="utf-8") as f:
        all_pages = json.load(f)
    # ---
    return all_pages


def mk_new():
    # ---
    all_pages = cat_cach.make_cash_to_cats(return_all_pages=True, print_s=False)
    # ---
    all_pages = [x for x in all_pages[:] if valid_title(x)]
    # ---
    return all_pages


def ؤ():
    # ---
    filename = Dir / "all_pages.json"
    # ---
    all_pages = from_cach(filename)
    # ---
    if not all_pages:
        # ---
        all_pages = mk_new()
        # ---
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(all_pages, f)
        except Exception as e:
            printe.output(e)
    # ---
    return all_pages
