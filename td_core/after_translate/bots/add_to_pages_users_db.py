#!/usr/bin/python3
"""

from after_translate.bots.add_to_pages_users_db import add_to_mdwiki_sql_users


"""
import logging

#
#
#
import sys
import time

from mdapi_sql import sql_for_mdwiki

# ---
from pymysql.converters import escape_string

logger = logging.getLogger(__name__)

cat_for_pages = {}
# from after_translate.bots.fixcat import cat_for_pages


pages_users = sql_for_mdwiki.get_all_pages_all_keys(table="pages_users")
pages_users_tab = {}

# { "id": 3186, "title": "Pemirolast", "lang": "ar", "user": "Mina karaca", "pupdate": "2024-03-23", "target": "user:Mina karaca/x", "add_date": "2024-04-14" }

for tab in pages_users:
    lang = tab["lang"]
    user = tab["user"]
    title = tab["title"]
    # ---
    pages_users_tab.setdefault(user, {})
    pages_users_tab[user].setdefault(lang, {})
    # ---
    pages_users_tab[user][lang][title] = tab


def add_new_row(mdtitle, lang, user, pupdate, target):
    mdtit = escape_string(mdtitle)
    user2 = escape_string(user)
    tar = escape_string(target)
    # ---
    add_date = time.strftime("%Y-%m-%d")
    # ---
    insert_qua_old = f"""
        INSERT INTO pages_users (title, lang, user, pupdate, target, add_date)
        SELECT '{mdtit}', '{lang}', '{user2}', '{pupdate}', '{tar}', '{add_date}'
        WHERE NOT EXISTS ( SELECT 1 FROM pages_users WHERE title='{mdtit}' AND lang='{lang}' AND user='{user2}');
        """
    # ---
    logger.info("______ \\/\\/\\/ _______")
    logger.info(insert_qua_old)
    # ---
    insert_qua = """
        INSERT INTO pages_users (title, lang, user, pupdate, target, add_date)
        SELECT %s, %s, %s, %s, %s, %s
        WHERE NOT EXISTS ( SELECT 1 FROM pages_users WHERE title=%s AND lang=%s AND user=%s);
        """
    # ---
    values = [mdtitle, lang, user, pupdate, target, add_date, mdtitle, lang, user]
    # ---
    sql_for_mdwiki.mdwiki_sql(insert_qua, values=values)


def update_row_new(mdtitle, lang, user, pupdate, target):
    # ---
    add_date = time.strftime("%Y-%m-%d")
    # ---
    update_qua_old = f"""
        UPDATE pages_users SET target = '{target}', pupdate = "{pupdate}",  add_date = "{add_date}"
        WHERE user = '{user}' AND title = '{mdtitle}' AND lang = "{lang}";"""
    # ---
    logger.info(update_qua_old)
    # ---
    update_qua = """
        UPDATE pages_users  SET target = %s, pupdate = %s,  add_date = %s
        WHERE user = %s AND title = %s AND lang = %s;
        """
    # ---
    values = [target, pupdate, add_date, user, mdtitle, lang]
    # ---
    sql_for_mdwiki.mdwiki_sql(update_qua, values=values)


def add_to_mdwiki_sql_users(lista):
    # Taba2 = {"mdtitle": md_title , "target": target, "user":user,"lang":lange,"pupdate":pupdate}
    # ---
    if "pages_users" not in sys.argv:
        logger.info('skip pages_users, <<green>> add "pages_users" to sys.argv to add it to pages_users')
        return
    # ---
    for _, tabe in lista.items():
        mdtitle = tabe["mdtitle"]
        lang = tabe["lang"]
        target = tabe["target"]
        user = tabe["user"]
        pupdate = tabe["pupdate"]
        # ---
        cat = cat_for_pages.get(mdtitle, "")
        # ---
        if not cat:
            logger.info(f"cat_for_pages.get({mdtitle}) = {cat}")
            # continue
        # ---
        is_in = pages_users_tab.get(user, {}).get(lang, {}).get(mdtitle)
        # ---
        if not is_in:
            add_new_row(mdtitle, lang, user, pupdate, target)
            continue
        # ---
        #  "pupdate", "target"
        if pupdate == is_in["pupdate"] and target == is_in["target"]:
            # logger.info(f"skip {mdtitle} {user} same result in sql..")
            continue
        # ---
        update_row_new(mdtitle, lang, user, pupdate, target)


if __name__ == "__main__":
    # python3 core8/pwb.py after_translate/bots/add_to_pages_users_db pages_users
    taba = [
        {
            "mdtitle": "Pem'irolast",
            "lang": "hhh",
            "user": "Mina karacax",
            "pupdate": "2024-03-23",
            "target": "مستخدم:اليمن",
            "add_date": "2024-04-14",
        }
    ]
    add_to_mdwiki_sql_users(taba)
