#!/usr/bin/python3
"""
بوت إضافة التصنيف للمقالات بدون تصنيف في قواعد البيانات

python3 core8/pwb.py td_core/after_translate/bots/fixcat

"""

import logging
import sys

import tqdm
from pymysql.converters import escape_string

from db.tools.services.session import get_session
from sqlalchemy import text
from mdwiki_api.mdwiki_page import CatDepth

logger = logging.getLogger(__name__)

# result_table = CatDepth(f"Category:{cat}", sitecode="www", family="mdwiki", depth=0, ns="0")
# ---
cat_for_pages = {}


def get_cats_and_pages() -> None:
    # ---
    with get_session() as session:
        sq = [dict(row._mapping) for row in session.execute(text("select category, depth from categories;"))]
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
    # logger.info(f'cat: {cat} , len: {lena}')
    # ---
    logger.info(f"<<yellow>> RTT_dpl: {RTT_dpl}")


get_cats_and_pages()


def get_pages_with_no_cat_old() -> None:
    # ---
    add_cat = {}
    # ---
    with get_session() as session:
        ioi = [dict(row._mapping) for row in session.execute(text("select title from pages where (cat = '' OR cat IS NULL);"))]
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
        logger.info("=======================")
        logger.info(quanew)
        # ---
        if "dont" not in sys.argv:
            with get_session() as session:
                session.execute(text(quanew))
                session.commit()


def get_pages_with_no_cat() -> None:
    # ---
    add_cat = {}
    cat_to_titles = {}
    # ---
    with get_session() as session:
        ioi = [dict(row._mapping) for row in session.execute(text("select title, cat from pages where cat in ('RTT', '') ;"))]
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
        if "dont" not in sys.argv:
            with get_session() as session:
                session.execute(
                    text("UPDATE pages SET cat = :cat WHERE title IN :titles"),
                    {"cat": cat, "titles": list(values)},
                )
                session.commit()
    # ---
    qua2 = "update pages set cat = 'RTT' where (cat = '' OR cat IS NULL); "
    # ---
    with get_session() as session:
        session.execute(text(qua2))
        session.commit()


if __name__ == "__main__":
    get_pages_with_no_cat()
