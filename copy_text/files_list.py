#!/usr/bin/python3
"""

python3 core8/pwb.py copy_text/files_list


"""
import json
import logging
import sys
from pathlib import Path

from apis.cat_cach import Cat_Depth
from mdapi_sql import sql_for_mdwiki

logger = logging.getLogger(__name__)

dir1 = Path(__file__).parent
Dir = "/data/project/medwiki/public_html/mdtexts"

if str(dir1).find("I:") != -1:
    Dir = "I:/medwiki/new/medwiki.toolforge.org_repo/public_html/mdtexts"

Dir = Path(Dir)


def fix_title(x):
    return x.replace(" ", "_").replace("'", "_").replace(":", "_").replace("/", "_").replace('"', "_")


def cats_pages():
    # ---
    all_pages = []
    to_cats = {}
    # ---
    cats = sql_for_mdwiki.get_db_categories()
    # ---
    # sort cats making RTT the last item
    cats = dict(sorted(cats.items(), key=lambda x: x[0] == "RTT"))
    # ---
    for cat, depth in cats.items():
        # ---
        ca = Cat_Depth(cat, depth=depth, ns="all", print_s=False)
        # ---
        ca_list = [x for x in ca if x not in all_pages]
        # ---
        logger.info(f"<<green>> ca_list({cat}): {len(ca_list)}")
        # ---
        to_cats[cat] = ca_list
        # ---
        all_pages.extend(ca_list)
    # ---
    return to_cats


def dump_titles(titles):
    # ---
    file = Dir / "cats_titles.json"
    # ---
    data = {}
    # ---
    if file.exists():
        # read data
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"<<yellow>> titles in titles.json: {len(data)}")
    # ---
    for cat, cat_titles in titles.items():
        new_data = {x: fix_title(x) for x in cat_titles if x not in data.get(cat, [])}
        logger.info(f"<<yellow>> cat_titles({cat}) in new_data: {len(new_data)}")
        # ---
        data.setdefault(cat, {})
        # ---
        # merge data
        data[cat].update(new_data)
    # ---
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    # ---
    return


def main():
    # ---
    all_pages = cats_pages()
    # ---
    print(f"all_pages: {len(all_pages)}")
    # ---
    dump_titles(all_pages)


if __name__ == "__main__":
    main()
