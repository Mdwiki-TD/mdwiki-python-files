#!/usr/bin/python3
"""

python3 core8/pwb.py apis/cat_cach

from md_core_helps.apis import cat_cach
from md_core_helps.apis.cat_cach import Cat_Depth
all_pages = cat_cach.from_cache()

"""
import json
import logging
import os
import stat
import sys
import time
from datetime import datetime
from pathlib import Path

from db.tools.services.content.category_service import list_categories_as_dict
from md_core_helps.bots.check_title import valid_title
from mdwiki_api.mdwiki_page import CatDepth
from td_core.td_dirs import paths

logger = logging.getLogger(__name__)

today = datetime.today().strftime("%Y-%m-%d")


def dump_it(file, data) -> bool:
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return True
    except Exception as e:
        logger.error(f"<<red>> Error: {e}")
    # ---
    return False


def from_cache() -> list[str]:
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
                logger.error(f"<<red>> Error reading cache file: {e}")
    # ----
    all_pages = make_cash_to_cats()
    # ---
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(all_pages))
    # ---
    return all_pages


def dump_to_cache(cat, data) -> None:
    # ---
    if cat.lower().startswith("category:"):
        cat = cat[9:]
    # ---
    filename = paths.cats_cash_path / f"{cat}.json"
    # ---
    if not filename.exists():
        filename.touch(mode=stat.S_IRWXU | stat.S_IRWXG)
        filename.write_text("[]")
    else:
        # Get the time of last modification of the file
        last_modified = datetime.fromtimestamp(os.path.getmtime(filename)).strftime("%Y-%m-%d")
        # ---
        # if last_modified != today:
        logger.info(f"<<purple>> last modified: {last_modified}, today: {today}. ")
    # ---
    datalist = data.get("list", [])
    # ---
    if not datalist:
        logger.error(f"<<red>> No data for {cat}")
        return
    # ---
    if dump_it(filename, data):
        len_data = len(data.get("list") or data)
        logger.info(f"<<green>> {cat}.json is updated ({len_data})")


def Cat_Depth(title, depth: int = 0, ns: str = "all", print_s: bool = True) -> list[str]:
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
    logger.info(
        f"<<blue>>CatDepth result<<yellow>> ({len(result_table)}) ns:{ns} in {title}, depth:{depth} in {delta} seconds"
    )
    # ---
    return list(result_table.keys())


def make_cash_to_cats(dump_data: bool = False) -> list[str]:
    # ---
    all_pages = []
    # ---
    cats = list_categories_as_dict()
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
            # logger.info(f"len of pages in {cat}: {len(members)}")
        # ---
        filename = Path(__file__).parent / "all_pages.json"
        # ---
        if dump_it(filename, all_pages):
            logger.info(f"<<green>> all_pages.json is updated ({len(all_pages)})")
    # ---
    return all_pages


if __name__ == "__main__":
    make_cash_to_cats(dump_data=True)
