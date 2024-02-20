#!/usr/bin/python3
"""

from after_translate.bots.add_to_mdwiki import add_to_mdwiki_sql
"""
#
# (C) Ibrahem Qasim, 2022
#
#
import sys
import time
from pymysql.converters import escape_string
# ---
from newapi import printe
from mdpy.bots import sql_for_mdwiki
from after_translate.bots.fixcat import cat_for_pages


def add_to_mdwiki_sql_users(lista):
    # Taba2 = {"mdtitle": md_title , "target": target, "user":user,"lang":lange,"pupdate":pupdate}
    # ---
    if 'pages_users' not in sys.argv:
        printe.output('skip pages_users, <<green>> add "pages_users" to sys.argv to add it to pages_users')
        return
    # ---
    for tabe in lista:
        mdtitle   = tabe['mdtitle']
        lang      = tabe['lang']
        target    = tabe['target']
        user      = tabe['user']
        pupdate   = tabe['pupdate']
        # ---
        cat = cat_for_pages.get(mdtitle, '')
        # ---
        if not cat:
            printe.output(f'cat_for_pages.get({mdtitle}) = {cat}')
            continue
        # ---
        mdtit = escape_string(mdtitle)
        user2 = escape_string(user)
        tar   = escape_string(target)
        # ---
        add_date = time.strftime("%Y-%m-%d")
        # ---
        update_qua = f'''
            UPDATE pages_users SET 
                target = '{tar}', pupdate = "{pupdate}",  add_date = "{add_date}" 
            WHERE user = '{user2}' 
            AND title = '{mdtit}'
            AND lang = "{lang}"
            ;'''
        # ---
        insert_qua = f'''
            INSERT INTO
                pages_users (title, lang, user, pupdate, target, add_date)
            SELECT 
                '{mdtit}', '{lang}', '{user2}', '{pupdate}', '{tar}', '{add_date}'
            WHERE NOT EXISTS ( SELECT 1 FROM pages_users WHERE title='{mdtit}' AND lang='{lang}' AND user='{user2}' )
            ;
            '''
        # ---
        printe.output('______ \\/\\/\\/ _______')
        # ---
        printe.output(update_qua)
        sql_for_mdwiki.mdwiki_sql(update_qua)
        # ---
        printe.output(insert_qua)
        sql_for_mdwiki.mdwiki_sql(insert_qua)


def add_to_mdwiki_sql(table, to_update_lang_user_mdtitle_x):
    # Taba2 = {"mdtitle": md_title , "target": target, "user":user,"lang":lange,"pupdate":pupdate}
    # ---
    lista = []
    # ---
    for _, tab in table.items():
        for tt in tab:
            tabe      = tab[tt]
            mdtitle   = tabe['mdtitle']
            lang      = tabe['lang']
            target    = tabe['target']
            user      = tabe['user']
            pupdate   = tabe['pupdate']
            namespace = tabe['namespace']
            # ---
            cat = cat_for_pages.get(mdtitle, '')
            # ---
            mdtit = escape_string(mdtitle)
            user2 = escape_string(user)
            tar   = escape_string(target)
            word  = 0
            # ---
            if str(namespace) != '0':
                lista.append(tabe)
                continue
            # ---
            uuu = ''
            # ---
            # date now format like 2023-01-01
            add_date = time.strftime("%Y-%m-%d")
            # ---
            update_qua = f'''
                UPDATE pages SET 
                    target = '{tar}',  pupdate = "{pupdate}",  add_date = "{add_date}" 
                WHERE user = '{user2}' 
                AND title = '{mdtit}'
                AND lang = "{lang}"
                ;'''
            # ---
            insert_qua = f'''
                INSERT INTO
                    pages (title, word, translate_type, cat, lang, date, user, pupdate, target, add_date)
                SELECT 
                    '{mdtit}', '{word}', 'lead', '{cat}', '{lang}', '{add_date}', '{user2}', '{pupdate}', '{tar}', '{add_date}'
                WHERE NOT EXISTS ( SELECT 1 FROM pages WHERE title='{mdtit}' AND lang='{lang}' AND user='{user2}' )
                ;
                '''
            # ---
            printe.output('______ \\/\\/\\/ _______')
            # ---
            # date1x = to_update_lang_user_mdtitle_x.get(lang, {}).get(user, [])
            date1x = to_update_lang_user_mdtitle_x.get(user, [])
            # ---
            # find if to update or to insert
            if mdtitle in date1x:
                printe.output(f'to update: title:{mdtitle}, user:{user} ')
                uuu = update_qua
            else:
                printe.output(f'to insert: title:{mdtitle}, user:{user} ')
                uuu = insert_qua
            # ---
            printe.output(uuu)
            # ---
            sql_for_mdwiki.mdwiki_sql(uuu)
    # ---
    add_to_mdwiki_sql_users(lista)
