#!/usr/bin/python3
"""
python3 core8/pwb.py md_core/mdpy/sql_for_mdwiki

# ---
from md_core_helps.mdapi_sql import sql_for_mdwiki
# sql_for_mdwiki. select_md_sql(query, return_dict=False, values=None)
# sql_for_mdwiki. mdwiki_sql(query, return_dict=False, values=None, many=False)
# sql_for_mdwiki. set_target_where_id(new_target, iid)
# sql_for_mdwiki. set_deleted_where_id(iid)
# sql_for_mdwiki. insert_to_pages_users_to_main(id, target, user, qid)
# sql_for_mdwiki. add_new_to_pages(tab)

# pages = sql_for_mdwiki.get_all_pages()
# cats = sql_for_mdwiki.get_db_categories() # title:depth
# users = sql_for_mdwiki.get_db_users() # list
# sql_for_mdwiki.get_all_pages_all_keys(lang=False)

# ---
"""
import logging
import time

from md_core_helps.mdapi_sql import sql_td_bot

logger = logging.getLogger(__name__)


def mdwiki_sql(
    query,
    return_dict=False,
    values=None,
    many=False,
    **kwargs,
):
    # ---
    if not query:
        logger.info("query == ''")
        return {}
    # ---
    return sql_td_bot.toolforge_tools_sql_connect(
        query,
        return_dict=return_dict,
        values=values,
        many=many,
        **kwargs,
    )


def mdwiki_sql_dict(
    query,
    values=None,
    many=False,
    **kwargs,
):
    # ---
    if not query:
        logger.info("query == ''")
        return {}
    # ---
    return sql_td_bot.toolforge_tools_sql_connect(
        query,
        return_dict=True,
        values=values,
        many=many,
        **kwargs,
    )


def select_md_sql(
    query,
    *args,
    **kwargs,
):
    # ---
    if not query:
        logger.info("query == ''")
        return {}
    # ---
    return mdwiki_sql(
        query,
        *args,
        **kwargs,
    )


def get_all_pages():
    return [ta["title"] for ta in select_md_sql("select DISTINCT title from pages;", return_dict=True)]


def get_all_from_table(table_name="enwiki_pageviews"):
    return select_md_sql(f"select DISTINCT * from {table_name};", return_dict=True)


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
    return list(select_md_sql(qua, return_dict=True))


def get_db_categories() -> dict:
    return {
        c["category"]: c["depth"] for c in
        select_md_sql("select category, depth from categories;", return_dict=True)
    }


def get_db_category_members() -> dict[str, list]:
    data: dict[str, list] = {}
    sql_result = select_md_sql("select category, article_id from category_members;", return_dict=True)

    for line in sql_result:
        if line["category"] not in data:
            data[line["category"]] = []
        data[line["category"]].append(line["article_id"])

    return data


def get_db_users() -> list:
    return [c["username"] for c in select_md_sql("select username from users;", return_dict=True)]


def set_target_where_id(new_target, iid):
    # ---
    logger.info(f"<<yellow>> () new_target:{new_target}, id:{iid}")
    # ---
    if new_target == "" or iid == "":
        return None
    # ---
    query = "UPDATE pages set target = %s where id = %s;"
    values = [new_target, iid]
    # ---
    return mdwiki_sql(query, return_dict=True, values=values)


def set_deleted_where_id(iid):
    # ---
    logger.info(f"<<yellow>> (), id:{iid}")
    # ---
    if iid == "":
        return None
    # ---
    query = "UPDATE pages set deleted = 1 where id = %s;"
    # ---
    return mdwiki_sql(query, return_dict=True, values=[iid])


def insert_to_pages_users_to_main(id, target, user, qid):
    # ---
    logger.info(f"<<yellow>> : {id}, {target=}, {user=}, {qid=}")
    # ---
    query = "insert into pages_users_to_main (id, new_target, new_user, new_qid) select %s, %s, %s, %s"
    # ---
    params = [id, target, user, qid]
    # ---
    mdwiki_sql(query, values=params)
    # ---
    qua = "select DISTINCT * from pages_users_to_main where id = %s and new_target = %s and new_user = %s and new_qid = %s"
    # ---
    find_it = mdwiki_sql_dict(qua, values=params)
    # ---
    if find_it:
        logger.info("<<green>> TRUE.. ")
        return True
    else:
        logger.info("<<red>> FALSE.. ")
        return False


def add_new_to_pages(tab):
    # ---
    date = time.strftime("%Y-%m-%d")
    # ---
    logger.info("______ \\/\\/\\/ _______")
    # ---
    insert_qua = """
        INSERT INTO pages (title, word, translate_type, cat, lang, user, target, date, pupdate, add_date)
        SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        WHERE NOT EXISTS ( SELECT 1 FROM pages WHERE title=%s AND lang=%s AND user=%s );
        """
    # ---
    values = [
        tab.get("title", ""),
        tab.get("word"),
        tab.get("translate_type", "lead"),
        tab.get("cat", "RTT"),
        tab.get("lang"),
        tab.get("user"),
        tab.get("target"),
        tab.get("date", date),
        tab.get("pupdate", date),
        tab.get("add_date", date),
        tab.get("title"),
        tab.get("lang"),
        tab.get("user"),
    ]
    # ---
    mdwiki_sql(insert_qua, values=values)
