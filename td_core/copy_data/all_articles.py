#!/usr/bin/python3
"""

python3 core8/pwb.py copy_data/all_articles
python3 core8/pwb.py copy_data/exists_db

"""

import os
import json
import sys
from mdapi_sql import sql_for_mdwiki
from newapi.mdwiki_page import CatDepth
from mdpyget.bots.to_sql import to_sql


def main():
    # ---
    data = {}
    # ---
    length = {}
    # ---
    cats = sql_for_mdwiki.get_db_categories()
    # ---
    if "RTT" in cats:
        del cats["RTT"]
    # ---
    for cat in cats.keys():
        # ---
        onlyns = 3000 if cat == "Videowiki scripts" else ""
        ns = 3000 if cat == "Videowiki scripts" else 0
        # ---
        mdwiki_pages = CatDepth(f"Category:{cat}", sitecode="www", family="mdwiki", depth=0, ns=ns, onlyns=onlyns)
        # ---
        titles = {dd: cat for dd in mdwiki_pages if dd not in data}
        # ---
        data.update(titles)
        # ---
        length[cat] = len(titles)
    # ---
    RTT_pages = CatDepth("Category:RTT", sitecode="www", family="mdwiki", depth=3, ns="0")
    # ---
    RTT_pages = {title: "RTT" for title in RTT_pages if title not in data}
    # ---
    length["RTT"] = len(RTT_pages)
    data.update(RTT_pages)
    # ---
    for cat, len_titles in length.items():
        print(f"Category:{cat}: {len_titles=}")
    # ---
    start_to_sql(data)


def start_to_sql(data):
    data2 = [{"article_id": title, "category": category} for title, category in data.items()]
    # ---
    to_sql(data2, "all_articles", ["article_id", "category"], title_column="article_id")


def test():
    # python3 core8/pwb.py copy_data/all_articles test
    # ---
    data = {"Asbestosis": "RTT", "Zoster vaccine": "RTT"}
    # ---
    start_to_sql(data)


if __name__ == "__main__":
    # ---
    if "test" in sys.argv:
        test()
        exit()
    # ---
    main()
