#!/usr/bin/python3
"""

python3 core8/pwb.py apis/cat_cach

from apis import cat_cach
from apis/cat_cach import Cat_Depth
all_pages = cat_cach.from_cache()

"""
import time
import sys
import os
import json
import stat
from datetime import datetime

from pathlib import Path
from mdapi_sql import sql_for_mdwiki
from mdpy.bots.check_title import valid_title
from newapi import printe
from newapi.mdwiki_page import CatDepth

# result_table = CatDepth(title, sitecode="www", family="mdwiki", depth=0, ns="all")

Day_History = datetime.now().strftime("%Y-%m-%d")

if os.getenv("HOME"):
    dump_path = os.getenv("HOME") + "/public_html/td/Tables/cats_cash"
else:
    dump_path = "I:/mdwiki/mdwiki/public_html/td/Tables/cats_cash"

dump_path = Path(dump_path)

today = datetime.today().strftime("%Y-%m-%d")


def dump_it(file, data):
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return True
    except Exception as e:
        printe.output(f"<<red>> Error: {e}")
    # ---
    return False


def from_cache():
    file = Path(__file__).parent / "all_pages.json"
    # ----
    if file.exists() and "nodone" not in sys.argv:
        # ---
        last_modified = datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y-%m-%d")
        # ---
        if last_modified == today:
            try:
                data = json.loads(file.read_text())
                return data
            except (json.JSONDecodeError, PermissionError) as e:
                printe.output(f"<<red>> Error reading cache file: {e}")
    # ----
    all_pages = make_cash_to_cats()
    # ---
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(all_pages))
    # ---
    return all_pages


def dump_to_cache(cat, data):
    # ---
    if cat.lower().startswith("category:"):
        cat = cat[9:]
    # ---
    filename = dump_path / f"{cat}.json"
    # ---
    if not filename.exists():
        filename.touch(mode=stat.S_IRWXU | stat.S_IRWXG)
        filename.write_text("[]")
    else:
        # Get the time of last modification of the file
        last_modified = datetime.fromtimestamp(os.path.getmtime(filename)).strftime("%Y-%m-%d")
        # ---
        # if last_modified != today:
        printe.output(f"<<purple>> last modified: {last_modified}, today: {today}. ")
    # ---
    datalist = data.get("list", [])
    # ---
    if not datalist:
        printe.output(f"<<red>> No data for {cat}")
        return
    # ---
    if dump_it(filename, data):
        len_data = len(data.get("list") or data)
        printe.output(f"<<green>> {cat}.json is updated ({len_data})")


def Cat_Depth(title, depth=0, ns="all", print_s=True):
    # ---
    if not title.startswith("Category:"):
        title = "Category:" + title
    # ---
    start = time.time()
    # ---
    result_table = CatDepth(title, sitecode="www", family="mdwiki", depth=0, ns="all", print_s=print_s, gcmlimit="max")
    # ---
    # result_table = {key: result_table[key] for key in result_table if valid_title(key)}
    result_table = dict(filter(lambda item: valid_title(item[0]), result_table.items()))
    # ---
    final = time.time()
    # ---
    delta = final - start
    # ---
    delta = round(delta, 5)
    # ---
    printe.output(f"<<blue>>CatDepth result<<yellow>> ({len(result_table)}) ns:{ns} in {title}, depth:{depth} in {delta} seconds")
    # ---
    return list(result_table.keys())


def make_cash_to_cats(dump_data=False):
    # ---
    all_pages = []
    # ---
    cats = sql_for_mdwiki.get_db_categories()
    # ---
    all_cats = {}
    # ---
    for cat, depth in cats.items():
        # ---
        ca = Cat_Depth(cat, depth=depth, ns="all", print_s=False)
        # ---
        all_cats[cat] = ca
        # ---
        all_pages.extend([x for x in ca if x not in all_pages])
    # ---
    if dump_data:
        for cat, members in all_cats.items():
            tab = {"list": members}
            dump_to_cache(cat, tab)
            # print(f"len of pages in {cat}: {len(members)}")
        # ---
        filename = Path(__file__).parent / "all_pages.json"
        # ---
        if dump_it(filename, all_pages):
            printe.output(f"<<green>> all_pages.json is updated ({len(all_pages)})")
    # ---
    return all_pages


if __name__ == "__main__":
    make_cash_to_cats(dump_data=True)
