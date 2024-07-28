#!/usr/bin/python3
"""

python3 core8/pwb.py apis/cat_cach

from apis import cat_cach
all_pages = cat_cach.make_cash_to_cats(return_all_pages=True)

"""
import time
from datetime import datetime
from pathlib import Path
from mdapi_sql import sql_for_mdwiki
from mdpy.bots.check_title import valid_title
from newapi.mdwiki_page import CatDepth
# result_table = CatDepth(title, sitecode="www", family="mdwiki", depth=0, ns="all")

Day_History = datetime.now().strftime("%Y-%m-%d")
Dir = str(Path(__file__).parents[0])
dir2 = Dir.replace("\\", "/").split("/pybot/")[0]


def Cat_Depth(title, depth=0, ns="all"):
    # ---
    if not title.startswith("Category:"):
        title = "Category:" + title
    # ---
    start = time.time()
    # ---
    result_table = CatDepth(title, sitecode="www", family="mdwiki", depth=0, ns="all")
    # ---
    # result_table = {key: result_table[key] for key in result_table if valid_title(key)}
    result_table = dict(filter(lambda item: valid_title(item[0]), result_table.items()))
    # ---
    final = time.time()
    # ---
    delta = final - start
    # ---
    print(f"<<lightblue>>cat_cach.py: find {len(result_table)} pages(ns:{str(ns)}) in {title}, depth:{depth} in {delta} seconds")
    # ---
    return list(result_table.keys())


def make_cash_to_cats(return_all_pages=False):
    # ---
    all_pages = []
    # ---
    cats = sql_for_mdwiki.get_db_categories()
    # ---
    lens = {}
    # ---
    for cat, depth in cats.items():
        # ---
        ca = Cat_Depth(cat, depth=depth, ns="all")
        # ---
        print(f"len of pages in {cat}, depth:{depth}, : %d" % len(ca))
        # ---
        lens[cat] = len(ca)
        # ---
        all_pages.extend([x for x in ca if x not in all_pages])
    # ---
    for cat, length in lens.items():
        print(f"len of pages in {cat}: {length}")
    # ---
    if return_all_pages:
        return all_pages


if __name__ == "__main__":
    make_cash_to_cats()
