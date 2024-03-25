#!/usr/bin/python3
"""
بوت قواعد البيانات
# ---
from api_sql import wiki_sql
# ---
# if wiki_sql.GET_SQL():
# result = wiki_sql.sql_new(qua, wiki="", printqua=False)
# result = wiki_sql.sql_new_title_ns(qua2, wiki="en", t1="title", t2="ns")
# ---
"""

#
# (C) Ibrahem Qasim, 2023
#
#
import sys
import time as tttime

from api_sql import sql_qu

# ---
from mdpy import printe

# ---
can_use_sql_db = sql_qu.can_use_sql_db
# results = sql_qu.make_sql_connect( query, db='', host='', update=False, Return=[], return_dict=False)


def GET_SQL():
    return can_use_sql_db[1]


def make_labsdb_dbs_p(wiki):  # host, dbs_p = make_labsdb_dbs_p('ar')
    # ---
    if wiki.endswith("wiki"):
        wiki = wiki[:-4]
    # ---
    wiki = wiki.replace("-", "_")
    # ---
    databases = {
        "be-x-old": "be_x_old",
        "be_tarask": "be_x_old",
        "be-tarask": "be_x_old",
    }
    # ---
    wiki = databases.get(wiki, wiki)
    # ---
    wiki = f"{wiki}wiki"
    dbs = wiki
    # ---
    host = f"{wiki}.analytics.db.svc.wikimedia.cloud"
    # ---
    dbs_p = f"{dbs}_p"
    # ---
    return host, dbs_p


def sql_new(queries, wiki="", printqua=False, values=[]):
    # ---
    printe.output(f"wiki_sql.py sql_new wiki '{wiki}'")
    # ---
    host, dbs_p = make_labsdb_dbs_p(wiki)
    # ---
    if printqua or "printsql" in sys.argv:
        printe.output(queries)
    # ---
    if not GET_SQL():
        return []
    # ---
    start = tttime.time()
    final = tttime.time()
    # ---
    rows = sql_qu.make_sql_connect(queries, db=dbs_p, host=host, return_dict=True, values=values)
    # ---
    final = tttime.time()
    # ---
    delta = int(final - start)
    # ---
    printe.output(f'wiki_sql.py sql_new len(encats) = "{len(rows)}", in {delta} seconds')
    # ---
    return rows


def Make_sql_many_rows(queries, wiki="", printqua=False, return_dict=False):
    # ---
    printe.output(f"wiki_sql.py Make_sql_many_rows wiki '{wiki}'")
    # ---
    host, dbs_p = make_labsdb_dbs_p(wiki)
    # ---
    if printqua or "printsql" in sys.argv:
        printe.output(queries)
    # ---
    if not GET_SQL():
        return []
    # ---
    start = tttime.time()
    final = tttime.time()
    # ---
    rows2 = sql_qu.make_sql_connect(queries, db=dbs_p, host=host, return_dict=return_dict)
    # ---
    final = tttime.time()
    # ---
    delta = int(final - start)
    # ---
    printe.output(f'wiki_sql.py Make_sql_many_rows len(encats) = "{len(rows2)}", in {delta} seconds')
    # ---
    return rows2


def sql_new_title_ns(queries, wiki="", t1="page_title", t2="page_namespace"):
    # ---
    lang = wiki
    # ---
    if lang.endswith("wiki"):
        lang = lang[:-4]
    # ---
    rows = sql_new(queries, wiki=wiki)
    # ---
    if t1 == "":
        t1 = "page_title"
    if t2 == "":
        t2 = "page_namespace"
    # ---
    newlist = []
    # ---
    ns_text_tab_ar = {
        "0": "",
        "1": "نقاش",
        "2": "مستخدم",
        "3": "نقاش المستخدم",
        "4": "ويكيبيديا",
        "5": "نقاش ويكيبيديا",
        "6": "ملف",
        "7": "نقاش الملف",
        "10": "قالب",
        "11": "نقاش القالب",
        "12": "مساعدة",
        "13": "نقاش المساعدة",
        "14": "تصنيف",
        "15": "نقاش التصنيف",
        "100": "بوابة",
        "101": "نقاش البوابة",
        "828": "وحدة",
        "829": "نقاش الوحدة",
    }
    # ---
    ns_text_tab_en = {
        "0": "",
        "1": "Talk",
        "2": "User",
        "3": "User talk",
        "4": "Project",
        "5": "Project talk",
        "6": "File",
        "7": "File talk",
        "8": "MediaWiki",
        "9": "MediaWiki talk",
        "10": "Template",
        "11": "Template talk",
        "12": "Help",
        "13": "Help talk",
        "14": "Category",
        "15": "Category talk",
        "100": "Portal",
        "101": "Portal talk",
        "828": "Module",
        "829": "Module talk",
    }
    # ---
    for row in rows:
        title = row.get(t1)
        ns = row.get(t2)
        # ---
        if str(ns) == "0":
            newlist.append(title)
            continue
        # ---
        ns_text = ns_text_tab_ar.get(str(ns))
        if lang != "ar":
            ns_text = ns_text_tab_en.get(str(ns))
        # ---
        if not ns_text:
            printe.output(f"no ns_text for {str(ns)}")
        # ---
        if title and ns:
            new_title = f"{ns_text}:{title}"
            newlist.append(new_title)
        else:
            printe.output(f"xa {str(row)}")
            newlist.append(row)
        # ---
    # ---
    return newlist
