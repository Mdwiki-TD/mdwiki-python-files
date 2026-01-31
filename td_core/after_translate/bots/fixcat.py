#!/usr/bin/python3
"""
بوت إضافة التصنيف للمقالات بدون تصنيف في قواعد البيانات

python3 core8/pwb.py after_translate/bots/fixcat

"""

import sys

import tqdm
from mdapi_sql import sql_for_mdwiki
from newapi import printe
from newapi.mdwiki_page import CatDepth
from pymysql.converters import escape_string

# result_table = CatDepth(f"Category:{cat}", sitecode="www", family="mdwiki", depth=0, ns="0")
# ---
cat_for_pages = {}


def get_cats_and_pages():
    # ---
    sq = sql_for_mdwiki.select_md_sql("select category, depth from categories;", return_dict=True)
    # ---
    catlen = {}
    # ---
    RTT_dpl = 0
    # ---
    for tab in sq:
        cat = tab["category"]
        depth = tab["depth"]
        # ---
        catlen[cat] = 0
        # ---
        pages = CatDepth(f"Category:{cat}", sitecode="www", family="mdwiki", depth=depth, ns="0", print_s=False)
        # ---
        for page in pages:
            if page in cat_for_pages:
                if cat != "RTT":
                    cat_for_pages[page] = cat
                    catlen[cat] += 1
                else:
                    RTT_dpl += 1
            else:
                cat_for_pages[page] = cat
                catlen[cat] += 1
    # ---
    # for cat, lena in catlen.items():
    # printe.output(f'cat: {cat} , len: {lena}')
    # ---
    printe.output(f"<<yellow>> RTT_dpl: {RTT_dpl}")


get_cats_and_pages()


def get_pages_with_no_cat_old():
    # ---
    add_cat = {}
    # ---
    ioi = sql_for_mdwiki.select_md_sql("select title from pages where (cat = '' OR cat IS NULL);", return_dict=True)
    # ---
    for tab in ioi:
        title = tab["title"]
        # ---
        cat = cat_for_pages.get(title, "")
        if cat != "":
            add_cat[title] = cat
    # ---
    for tit, cat in add_cat.items():
        # ---
        tit2 = escape_string(tit)
        # ---
        quanew = f"""UPDATE pages SET cat = '{cat}' WHERE title = '{tit2}';"""
        # ---
        printe.output("=======================")
        printe.output(quanew)
        # ---
        if "dont" not in sys.argv:
            qu = sql_for_mdwiki.mdwiki_sql(quanew, update=True)
            # ---
            printe.output(qu)


def get_pages_with_no_cat():
    # ---
    add_cat = {}
    cat_to_titles = {}
    # ---
    ioi = sql_for_mdwiki.select_md_sql("select title, cat from pages where cat in ('RTT', '') ;", return_dict=True)
    # ---
    for tab in tqdm.tqdm(ioi):
        title = tab["title"]
        cat_in = tab["cat"]
        # ---
        cat = cat_for_pages.get(title, "")
        # ---
        if cat_in == cat:
            continue
        # ---
        if cat:
            add_cat[title] = cat
            # ---
            cat_to_titles.setdefault(cat, []).append(title)
    # ---
    for cat, titles in cat_to_titles.items():
        # ---
        values = list(set(titles))
        # ---
        place_holder = ", ".join(["%s"] * len(values))
        # ---
        quanew = f"""UPDATE pages SET cat = '{cat}' WHERE title in ({place_holder});"""
        # ---
        printe.output("=======================")
        printe.output(quanew)
        # ---
        if "dont" not in sys.argv:
            # qu = sql_for_mdwiki.mdwiki_sql(quanew, update=True)
            qu = sql_for_mdwiki.mdwiki_sql(quanew, values=values, update=True)
            # ---
            printe.output(qu)
    # ---
    qua2 = "update pages set cat = 'RTT' where (cat = '' OR cat IS NULL); "
    # ---
    sql_for_mdwiki.mdwiki_sql(qua2, update=True)


if __name__ == "__main__":
    get_pages_with_no_cat()
