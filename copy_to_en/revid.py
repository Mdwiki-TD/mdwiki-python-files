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
file2 = Path(dir2) / "public_html" / "publish" / "all_pages_revids.json"


def dump(revids):
    """Dump a list of revision IDs to two JSON files.

    This function takes a list of revision IDs and writes them to two
    separate JSON files. It first writes to the file specified by the
    variable `file`, and then attempts to write to another file specified by
    the variable `file2`. The function also outputs the length of the list
    of revision IDs and logs the success or failure of each file write
    operation.

    Args:
        revids (list): A list of revision IDs to be dumped into JSON files.

    Note:
        The variables `file` and `file2` should be defined in the scope where
        this function is called.
    """

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
    """Retrieve the subcategories of a given category title.

    This function checks if the provided title starts with "Category:". If
    not, it prepends "Category:" to the title. It then creates an instance
    of the `CategoryDepth` class to query the subcategories and their
    revision IDs. The results are filtered to include only valid titles
    before being returned.

    Args:
        title (str): The title of the category to query.
        depth (int?): The depth of the category query. Defaults to 0.

    Returns:
        dict: A dictionary containing valid subcategory titles and their corresponding
            revision IDs.
    """

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
    """Retrieve all revision IDs from the database categories.

    This function fetches categories from the database and iterates through
    them to collect revision IDs. For each category, it creates an instance
    of `Cat_Depth` with the category name and its depth, then updates a
    dictionary with the revision IDs. Finally, it dumps the collected
    revision IDs for further use.

    Returns:
        dict: A dictionary containing revision IDs associated with their respective
            categories.
    """

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
