#!/usr/bin/python3
"""
python3 core8/pwb.py mdpy/sql_for_mdwiki

# ---
from mdpy.bots import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query, return_dict=False, values=None)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# pages = sql_for_mdwiki.get_all_pages()
# cats = sql_for_mdwiki.get_db_categories() # title:depth
# sql_for_mdwiki.add_titles_to_qids(tab, add_empty_qid=False)
# sql_for_mdwiki.set_title_where_qid(new_title, qid)
# sql_for_mdwiki.set_target_where_id(new_target, iid)
# sql_for_mdwiki.set_deleted_where_id(iid)
# sql_for_mdwiki.get_all_pages_all_keys(lang=False)
# ---

"""
import sys
import pymysql

# ---
from mdpy import printe
from pywikibot import config
from newapi import pymysql_bot

# result = pymysql_bot.sql_connect_pymysql(query, return_dict=False, values=None, main_args={}, credentials={}, conversions=None)
# ---
conversions = pymysql.converters.conversions
conversions[pymysql.FIELD_TYPE.DATE] = lambda x: str(x)
# ---
can_use_sql_db = {1: True}
# ---
from pathlib import Path

Dir = str(Path(__file__).parents[0])
# print(f'Dir : {Dir}')
# ---
dir2 = Dir.replace("\\", "/")
dir2 = dir2.split("/mdwiki/")[0] + "/mdwiki"
# ---
db_username = config.db_username
db_password = config.db_password
# ---
if config.db_connect_file is None:
    credentials = {"user": db_username, "password": db_password}
else:
    credentials = {"read_default_file": config.db_connect_file}
# ---
main_args = {
    "host": "tools.db.svc.wikimedia.cloud",
    "db": "s54732__mdwiki",
    "charset": "utf8mb4",
    # 'collation':  'utf8_general_ci',
    "use_unicode": True,
    "autocommit": True,
}
# ---
if "localhost" in sys.argv or dir2 == "I:/mdwiki":
    main_args["host"] = "127.0.0.1"
    main_args["db"] = "mdwiki"
    credentials = {"user": "root", "password": "root11"}


def sql_connect_pymysql(query, return_dict=False, values=None):
    # ---
    results = pymysql_bot.sql_connect_pymysql(query, return_dict=return_dict, values=values, main_args=main_args, credentials=credentials, conversions=conversions)
    # ---
    return results


def mdwiki_sql(query, return_dict=False, values=None, **kwargs):
    # ---
    if not can_use_sql_db[1]:
        print("no mysql")
        return {}
    # ---
    if not query:
        print("query == ''")
        return {}
    # ---
    # print('<<lightyellow>> newsql::')
    return sql_connect_pymysql(query, return_dict=return_dict, values=values)


def get_all_qids():
    # ---
    sq = mdwiki_sql("select DISTINCT title, qid from qids;", return_dict=True)
    return {ta["title"]: ta["qid"] for ta in sq}


def get_all_pages():
    return [ta["title"] for ta in mdwiki_sql("select DISTINCT title from pages;", return_dict=True)]


def get_all_pages_all_keys(lang=False, table="pages"):
    lang_line = ""
    # ---
    if lang:
        lang_line = f' where lang = "{lang}"'
    # ---
    if table not in ["pages", "pages_users"]:
        table = "pages"
    # ---
    qua = f"select DISTINCT * from {table} {lang_line};"
    return [ta for ta in mdwiki_sql(qua, return_dict=True)]


def get_db_categories():
    return {c["category"]: c["depth"] for c in mdwiki_sql("select category, depth from categories;", return_dict=True)}


def add_qid(title, qid):
    printe.output(f"<<yellow>> add_qid()  title:{title}, qid:{qid}")
    # ---
    qua = "INSERT INTO qids (title, qid) SELECT %s, %s;"
    # ---
    values = [title, qid]
    # ---
    return mdwiki_sql(qua, return_dict=True, values=values)


def set_qid_where_title(title, qid):
    # ---
    printe.output(f"<<yellow>> set_qid_where_title()  title:{title}, qid:{qid}")
    # ---
    qua = "UPDATE qids set qid = %s where title = %s;"
    values = [qid, title]
    # ---
    return mdwiki_sql(qua, return_dict=True, values=values)


def set_title_where_qid(new_title, qid):
    # ---
    printe.output(f"<<yellow>> set_title_where_qid()  new_title:{new_title}, qid:{qid}")
    # ---
    qua = "UPDATE qids set title = %s where qid = %s;"
    values = [new_title, qid]
    # ---
    return mdwiki_sql(qua, return_dict=True, values=values)


def set_target_where_id(new_target, iid):
    # ---
    printe.output(f"<<yellow>> set_target_where_id() new_target:{new_target}, id:{iid}")
    # ---
    if new_target == "" or iid == "":
        return
    # ---
    query = "UPDATE pages set target = %s where id = %s;"
    values = [new_target, iid]
    # ---
    return mdwiki_sql(query, return_dict=True, values=values)


def set_deleted_where_id(iid):
    # ---
    printe.output(f"<<yellow>> set_deleted_where_id(), id:{iid}")
    # ---
    if iid == "":
        return
    # ---
    query = "UPDATE pages set deleted = 1 where id = %s;"
    # ---
    return mdwiki_sql(query, return_dict=True, values=[iid])


def add_titles_to_qids(tab, add_empty_qid=False):
    # ---
    new = {}
    # ---
    for title, qid in tab.items():
        # ---
        if not title:
            print("title == ''")
            continue
        # ---
        if qid == "" and not add_empty_qid:
            print("qid == ''")
            continue
        # ---
        new[title] = qid
    # ---
    all_in = get_all_qids()
    # ---
    for title, qid in new.items():
        if title not in all_in:
            add_qid(title, qid)
            continue
        # ---
        q_in = all_in[title]
        # ---
        if qid != "":
            if not q_in:
                set_qid_where_title(title, qid)
            else:
                # set_qid_where_title(title, qid)
                printe.output(f"<<yellow>> set_qid_where_title() qid_in:{q_in}, new_qid:{qid}")
