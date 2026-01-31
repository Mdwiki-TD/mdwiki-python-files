#!/usr/bin/python3
"""
from mdpyget.pages_list import get_links_from_cats
"""
from mdapi_sql import sql_for_mdwiki
from mdpy.bots.check_title import valid_title
from newapi.mdwiki_page import CatDepth

videos_cats = ["Videowiki scripts", "RTTVideo"]


def get_links_from_cats(getcat=""):
    # ---
    titles = []
    # ---
    cac = sql_for_mdwiki.get_db_categories()
    # ---
    for cat, dep in cac.items():
        # ---
        if getcat != "" and cat != getcat:
            continue
        # ---
        is_video_cat = cat in videos_cats or "video" in cat.lower()
        onlyns = 3000 if is_video_cat else ""
        ns = 3000 if is_video_cat else 0
        # ---
        mdwiki_pages = CatDepth(f"Category:{cat}", sitecode="www", family="mdwiki", depth=dep, ns=ns, onlyns=onlyns)
        # ---
        titles.extend([dd for dd in mdwiki_pages if valid_title(dd) and dd not in titles])
    # ---
    return titles
