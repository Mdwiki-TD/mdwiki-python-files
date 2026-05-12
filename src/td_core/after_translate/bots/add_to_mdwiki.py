#!/usr/bin/python3
"""

from after_translate.bots.add_to_mdwiki import add_to_mdwiki_sql

"""
import logging
import sys
import time

from after_translate.bots.add_to_pages_users_db import add_to_mdwiki_sql_users
from after_translate.bots.fixcat import cat_for_pages
from mdapi_sql import sql_for_mdwiki

# ---
from pymysql.converters import escape_string

logger = logging.getLogger(__name__)


def add_new_row(mdtitle, lang, user, pupdate, target, word, cat):
    # ---
    mdtit = escape_string(mdtitle)
    user2 = escape_string(user)
    tar = escape_string(target)
    # ---
    add_date = time.strftime("%Y-%m-%d")
    # ---
    insert_qua_old = f"""
        INSERT INTO pages (title, word, translate_type, cat, lang, date, user, pupdate, target, add_date)
        SELECT '{mdtit}', '{word}', 'lead', '{cat}', '{lang}', '{add_date}', '{user2}', '{pupdate}', '{tar}', '{add_date}'
        WHERE NOT EXISTS ( SELECT 1 FROM pages WHERE title='{mdtit}' AND lang='{lang}' AND user='{user2}' );
        """
    # ---
    logger.info("______ \\/\\/\\/ _______")
    logger.info(insert_qua_old)
    # ---
    insert_qua = """
        INSERT INTO pages (title, word, translate_type, cat, lang, date, user, pupdate, target, add_date)
        SELECT %s, %s, 'lead', %s, %s, %s, %s, %s, %s, %s
        WHERE NOT EXISTS ( SELECT 1 FROM pages WHERE title=%s AND lang=%s AND user=%s );
        """
    # ---
    values = [mdtitle, word, cat, lang, add_date, user, pupdate, target, add_date, mdtitle, lang, user]
    # ---
    sql_for_mdwiki.mdwiki_sql(insert_qua, values=values)


def update_row_new(mdtitle, lang, user, pupdate, target):
    # ---
    mdtit = escape_string(mdtitle)
    user2 = escape_string(user)
    tar = escape_string(target)
    # ---
    add_date = time.strftime("%Y-%m-%d")
    # ---
    update_qua_old = f"""
        UPDATE pages SET target = '{tar}', pupdate = "{pupdate}", add_date = "{add_date}"
        WHERE user = '{user2}' AND title = '{mdtit}' AND lang = "{lang}";"""
    # ---
    logger.info(update_qua_old)
    # ---
    update_qua = """
        UPDATE pages SET target = %s, pupdate = %s, add_date = %s
        WHERE user = %s AND title = %s AND lang = %s;
        """
    # ---
    values = [target, pupdate, add_date, user, mdtitle, lang]
    # ---
    sql_for_mdwiki.mdwiki_sql(update_qua, values=values)


def add_to_pages_db(lange, tab, to_updatex):
    # Taba2 = {"mdtitle": md_title , "target": target, "user":user,"lang":lange,"pupdate":pupdate}
    # ---
    for _, tabe in tab.items():
        # tabe = { "mdtitle": md_title, "target": target, "user": user, "lang": lange, "pupdate": pupdate, "namespace": ns, }
        # ---
        mdtitle = tabe["mdtitle"]
        lang = tabe["lang"]
        target = tabe["target"]
        user = tabe["user"]
        pupdate = tabe["pupdate"]
        namespace = tabe["namespace"]
        # ---
        cat = cat_for_pages.get(mdtitle, "")
        # ---
        word = 0
        # ---
        if str(namespace) != "0":
            continue
        # ---
        # date1x = to_updatex.get(lang, {}).get(user, [])
        date1x = to_updatex.get(user, [])
        # ---
        # find if to update or to insert
        if mdtitle in date1x:
            logger.info(f"to update: title:{mdtitle}, user:{user} ")
            update_row_new(mdtitle, lang, user, pupdate, target)
        else:
            logger.info(f"to insert: title:{mdtitle}, user:{user} ")
            add_new_row(mdtitle, lang, user, pupdate, target, word, cat)


def add_to_mdwiki_sql(lange, tab, to_updatex):
    # Taba2 = {"mdtitle": md_title , "target": target, "user":user,"lang":lange,"pupdate":pupdate}
    # ---
    logger.info("<<red>> :: ")
    # ---
    ns0_pages = {x: va for x, va in tab.items() if str(va["namespace"]) == "0"}
    ns2_pages = {x: va for x, va in tab.items() if str(va["namespace"]) != "0"}
    # ---
    add_to_pages_db(lange, ns0_pages, to_updatex)
    # ---
    add_to_mdwiki_sql_users(ns2_pages)
