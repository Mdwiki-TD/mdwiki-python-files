#!/usr/bin/python3
"""

tfj run revid --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py copy_to_en/revid"

"""
import os
import json
from pathlib import Path
from newapi import printe

from mdapi_sql import sql_for_mdwiki
from mdpy.bots.check_title import valid_title
from newapi.mdwiki_page import CategoryDepth

Dir = Path(__file__).parent
dir2 = os.getenv("HOME")
# ---
if not dir2:
    dir2 = "I:/mdwiki"
# ---
file = Dir / "all_pages_revids.json"
# ---
file2 = Path(dir2) / "public_html" / "Translation_Dashboard" / "publish" / "all_pages_revids.json"


def dump(revids):
    printe.output(f"len(revids): {len(revids)}")
    # ---
    with open(file, "w", encoding="utf-8") as f:
        json.dump(revids, f, ensure_ascii=False)
        printe.output(f"<<blue>> dump to {file}")
    # ---
    try:
        with open(file2, "w", encoding="utf-8") as f:
            json.dump(revids, f, ensure_ascii=False)
            printe.output(f"<<blue>> dump to {file2}")
    except Exception as e:
        printe.output(f"<<red>> dump to {file2} error: {e}")


def Cat_Depth(title, depth=0):
    # ---
    if not title.startswith("Category:"):
        title = "Category:" + title
    # ---
    bot = CategoryDepth(title, sitecode="www", family="mdwiki", depth=0, ns="all", gcmlimit="max")
    # ---
    result_table = bot.subcatquery_()
    # ---
    result_table = bot.revids
    # ---
    # result_table = {key: result_table[key] for key in result_table if valid_title(key)}
    result_table = dict(filter(lambda item: valid_title(item[0]), result_table.items()))
    # ---
    printe.output(f"<<blue>>CatDepth result<<yellow>> ({len(result_table)}) in {title}, depth:{depth}.")
    # ---
    return result_table


def get_all_revids():
    # ---
    revids = {}
    # ---
    cats = sql_for_mdwiki.get_db_categories()
    # ---
    for cat, depth in cats.items():
        # ---
        ca = Cat_Depth(cat, depth=depth)
        # ---
        revids.update(ca)
    # ---
    dump(revids)


if __name__ == "__main__":
    get_all_revids()
    # d = Cat_Depth("RTTHearing", 0)
    # print(d)
