#!/usr/bin/python3
"""
بوت إضافة التصنيف للمقالات بدون تصنيف في قواعد البيانات

python3 core8/pwb.py after_translate/bots/fixcat

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import sys
from pymysql.converters import escape_string
from mdapi_sql import sql_for_mdwiki
from newapi import printe
from newapi.mdwiki_page import CatDepth
# result_table = CatDepth(f"Category:{cat}", sitecode="www", family="mdwiki", depth=0, ns="0")
# ---
cat_for_pages = {}


def get_cats_and_pages():
    # ---
    sq = sql_for_mdwiki.mdwiki_sql('select category, depth from categories;', return_dict=True)
    # ---
    catlen = {}
    # ---
    RTT_dpl = 0
    # ---
    for tab in sq:
        cat = tab['category']
        depth = tab['depth']
        # ---
        catlen[cat] = 0
        # ---
        pages = CatDepth(f"Category:{cat}", sitecode="www", family="mdwiki", depth=depth, ns="0")
        # ---
        for page in pages:
            if page in cat_for_pages:
                if cat != 'RTT':
                    cat_for_pages[page] = cat
                    catlen[cat] += 1
                else:
                    RTT_dpl += 1
            else:
                cat_for_pages[page] = cat
                catlen[cat] += 1
        # ---
    # ---
    # for cat, lena in catlen.items():
        # printe.output(f'cat: {cat} , len: {lena}')
    # ---
    printe.output(f'<<lightyellow>> RTT_dpl: {RTT_dpl}')


get_cats_and_pages()


def get_pages_with_no_cat():
    # ---
    add_cat = {}
    # ---
    ioi = sql_for_mdwiki.mdwiki_sql("select title from pages where cat = '';", return_dict=True)
    # ---
    for tab in ioi:
        title = tab['title']
        # ---
        cat = cat_for_pages.get(title, '')
        if cat != '':
            add_cat[title] = cat
    # ---
    for tit, cat in add_cat.items():
        # ---
        tit2 = escape_string(tit)
        # ---
        quanew = f"""UPDATE pages SET cat = '{cat}' WHERE title = '{tit2}';"""
        # ---
        printe.output('=======================')
        printe.output(quanew)
        # ---
        if 'dont' not in sys.argv:
            qu = sql_for_mdwiki.mdwiki_sql(quanew, update=True)
            # ---
            printe.output(qu)


if __name__ == '__main__':
    get_pages_with_no_cat()
