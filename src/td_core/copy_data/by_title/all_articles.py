#!/usr/bin/python3
"""

python3 core8/pwb.py td_core/copy_data/by_title/all_articles
python3 core8/pwb.py td_core/copy_data/by_title/exists_db

"""
import logging
import sys

from md_core_helps.mdapi_sql import sql_for_mdwiki
from mdwiki_api.mdwiki_page import CatDepth
from td_core.mdpyget.bots.to_sql import to_sql, insert_dict

logger = logging.getLogger(__name__)


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
    videos_cats = ["Videowiki scripts", "RTTVideo"]
    # ---
    to_add_category_members = {}
    # ---
    for cat in cats.keys():
        # ---
        is_video_cat = cat in videos_cats or "video" in cat.lower()
        onlyns = 3000 if is_video_cat else ""
        ns = 3000 if is_video_cat else 0
        # ---
        mdwiki_pages = CatDepth(f"Category:{cat}", sitecode="www", family="mdwiki", depth=0, ns=ns, onlyns=onlyns)
        # ---
        titles = {dd: cat for dd in mdwiki_pages if dd not in data}
        # ---
        data.update(titles)
        # ---
        to_add_category_members[cat] = list(mdwiki_pages)
        # ---
        length[cat] = len(titles)
    # ---
    RTT_pages = CatDepth("Category:RTT", sitecode="www", family="mdwiki", depth=3, ns="0")
    # ---
    to_add_category_members["RTT"] = list(RTT_pages)
    # ---
    rtt_pages_subs = {title: "RTT" for title in RTT_pages if title not in data}
    # ---
    length["RTT"] = len(rtt_pages_subs)
    data.update(rtt_pages_subs)
    # ---s
    for cat, len_titles in length.items():
        logger.info(f"Category:{cat}: {len_titles=}")
    # ---
    start_to_sql(data)
    # ---
    add_category_members_to_sql(to_add_category_members)


def add_category_members_to_sql(to_add_category_members):
    # ---
    data2 = []
    # ---
    db_category_members = sql_for_mdwiki.get_db_category_members()
    # ---
    for category, titles_from_mdwiki in to_add_category_members.items():
        # ---
        cats_in_db = db_category_members.get(category, [])
        # ---
        not_in = [{"category": category, "article_id": title} for title in titles_from_mdwiki if title not in cats_in_db]
        # ---
        logger.info(f"Category:{category}: {len(titles_from_mdwiki)=}, {len(cats_in_db)=}")
        data2.extend(not_in)
    # ---
    insert_dict(data2, "category_members", ["article_id", "category"])


def start_to_sql(data):
    data2 = [{"article_id": title, "category": category} for title, category in data.items()]
    # ---
    to_sql(data2, "all_articles", ["article_id", "category"], title_column="article_id")


def test():
    # python3 core8/pwb.py td_core/copy_data/all_articles test
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
