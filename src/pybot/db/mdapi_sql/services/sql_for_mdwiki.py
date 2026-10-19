#!/usr/bin/python3
""" """

import logging
import time
from typing import Any

from db.mdapi_sql.sql_td_bot import tf_sql_connect_dict, tf_sql_connect_update

logger = logging.getLogger(__name__)


def mdwiki_sql_update(
    query: str,
    values: list | tuple | None = None,
    many: bool = False,
) -> None | bool:
    # ---
    if not query:
        logger.info("query == ''")
        return None
    # ---
    return tf_sql_connect_update(
        query=query,
        values=values,
        many=many,
    )


def mdwiki_sql_dict(
    query: str,
    values: list | tuple | None = None,
    many: bool = False,
    **kwargs,
) -> list[dict[str, Any]]:
    # ---
    if not query:
        logger.info("query == ''")
        return []
    # ---
    result = tf_sql_connect_dict(
        query,
        values=values,
        many=many,
        **kwargs,
    )
    return result


def get_all_pages() -> list[str]:
    return [ta["title"] for ta in mdwiki_sql_dict("select DISTINCT title from pages;")]


def get_all_from_table(table_name: str = "enwiki_pageviews") -> list[dict[str, Any]]:
    return mdwiki_sql_dict(f"select DISTINCT * from {table_name};")


def get_all_pages_all_keys(lang: str | None = None, table: str = "pages") -> list[Any]:
    lang_line = ""
    # ---
    if lang:
        lang_line = f' where lang = "{lang}"'
    # ---
    if table not in ["pages", "pages_users"]:
        table = "pages"
    # ---
    qua = f"select DISTINCT * from {table} {lang_line};"
    return mdwiki_sql_dict(qua)


def get_db_categories() -> dict[str, Any]:
    result = mdwiki_sql_dict("select category, depth from categories;")
    return {c["category"]: c["depth"] for c in result}


def get_db_category_members() -> dict[str, list]:
    data: dict[str, list] = {}
    sql_result = mdwiki_sql_dict("select category, article_id from category_members;")

    for line in sql_result:
        if line["category"] not in data:
            data[line["category"]] = []
        data[line["category"]].append(line["article_id"])

    return data


def get_db_users() -> list:
    return [c["username"] for c in mdwiki_sql_dict("select username from users;")]


def set_target_where_id(new_target, iid) -> None | list[dict[str, Any]]:
    # ---
    logger.info(f"<<yellow>> () new_target:{new_target}, id:{iid}")
    # ---
    if new_target == "" or iid == "":
        return None
    # ---
    query = "UPDATE pages set target = %s where id = %s;"
    values = [new_target, iid]
    # ---
    return mdwiki_sql_dict(query, values=values)


def set_deleted_where_id(iid) -> None | list[dict[str, Any]]:
    # ---
    logger.info(f"<<yellow>> (), id:{iid}")
    # ---
    if iid == "":
        return None
    # ---
    query = "UPDATE pages set deleted = 1 where id = %s;"
    # ---
    return mdwiki_sql_dict(query, values=[iid])


def insert_to_pages_users_to_main(id, target, user, qid) -> bool:
    # ---
    logger.info(f"<<yellow>> : {id}, {target=}, {user=}, {qid=}")
    # ---
    query = "insert into pages_users_to_main (id, new_target, new_user, new_qid) select %s, %s, %s, %s"
    # ---
    params = [id, target, user, qid]
    # ---
    mdwiki_sql_update(query, values=params)
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


def add_new_to_pages(tab) -> None:
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
    mdwiki_sql_update(insert_qua, values=values)
