#!/usr/bin/python3
"""
from mdpyget.pages_list import get_links_from_cats
"""
from mdapi_sql import sql_for_mdwiki
from newapi.mdwiki_page import CatDepth
from mdpy.bots.check_title import valid_title


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
        onlyns = 3000 if cat == "Videowiki scripts" else ""
        ns = 3000 if cat == "Videowiki scripts" else 0
        # ---
        mdwiki_pages = CatDepth(f"Category:{cat}", sitecode="www", family="mdwiki", depth=dep, ns=ns, onlyns=onlyns)
        # ---
        titles.extend([dd for dd in mdwiki_pages if valid_title(dd) and dd not in titles])
    # ---
    return titles
