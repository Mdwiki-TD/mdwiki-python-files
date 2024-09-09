#!/usr/bin/python3
"""
https://hashtags.wmcloud.org/json/?query=mdwikicx

بوت قواعد البيانات

python3 core8/pwb.py after_translate/sql_new
python3 core8/pwb.py after_translate/sql_new pages_users
python3 core8/pwb.py after_translate/sql_new justsql break
python3 core8/pwb.py after_translate/sql_new justsql
python3 core8/pwb.py after_translate/sql_new -lang:ur

"""

import sys
import time

from newapi import printe

from after_translate.bots.get_pages import get_pages_from_db
from after_translate.bots import add_to_wd
from after_translate.bots.add_to_mdwiki import add_to_mdwiki_sql
from after_translate import start_work

# ---
from mdapi_sql import wiki_sql

# ---
skip_langs = ["zh-yue", "ceb"]
# ---
query_main = """
    SELECT
        DISTINCT p.page_title AS title,
        SUBSTRING_INDEX(SUBSTRING_INDEX(c.comment_text, 'Ibrahem/', -1), ']]', 1) AS comment_text,
        a.actor_name,
        r.rev_timestamp,
        p.page_namespace,
        r.rev_parent_id
    FROM
        change_tag t
        INNER JOIN change_tag_def ctd ON ctd.ctd_id = t.ct_tag_id
        INNER JOIN revision r ON r.rev_id = t.ct_rev_id
        INNER JOIN actor a ON r.rev_actor = a.actor_id
        INNER JOIN comment c ON c.comment_id = r.rev_comment_id
        INNER JOIN page p ON r.rev_page = p.page_id
    WHERE
        ctd.ctd_name in (
            "contenttranslation",
            "contenttranslation-v2"
        ) #id = 3 # id = 120
        # AND r.rev_parent_id = 0
        # AND r.rev_timestamp > 20210101000000
        AND r.rev_timestamp > 20240101000000
        AND comment_text like "%User:Mr. Ibrahem/%" #AND p.page_namespace = 0
    GROUP BY
        p.page_title,
        a.actor_name,
        c.comment_text
    """


def sql_results(lang):
    # ---
    qua = query_main
    # ---
    qua += "\n;"
    # ---
    if "printquery" in sys.argv:
        print(qua)
    # ---
    result = wiki_sql.sql_new(qua, str(lang))
    return result


def main():
    # ---
    lang_o = ""
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg in ["lang", "-lang"]:
            lang_o = value
    # ---
    to_update, langs_to_t_u, targets_done, tit_user_lang, targets_done_by_mdtitle = get_pages_from_db(lang_o)
    # ---
    time.sleep(3)
    # ---
    numb_lang = 0
    lnn = len(langs_to_t_u.keys())
    # ---
    for lange in langs_to_t_u:
        # ---
        numb_lang += 1
        # ---
        printe.output(" \\/\\/\\/\\/\\/ ")
        printe.output(f'mdwiki/after_translate/sql.py: {numb_lang} Lang from {lnn} : "{lange}"')
        # ---
        if lange in skip_langs:
            printe.output(f"skip lang:{lange}")
            continue
        # ---
        result = sql_results(lange)
        # ---
        tgd = targets_done.get(lange, {})
        tgd_by_md = targets_done_by_mdtitle.get(lange, {})
        # ---
        if not result:
            printe.output("no result")
            continue
        # ---
        lang_tab = start_work.start(result, lange, tgd, tgd_by_md, tit_user_lang)
        # ---
        if "only" in sys.argv:
            continue
        # ---
        if "justsql" not in sys.argv:
            add_to_wd.add_tab_to_wd({lange: lang_tab})
        # ---
        # add_to_mdwiki_sql({lange: lang_tab}, to_update.get(lange, {}))
        add_to_mdwiki_sql(lange, lang_tab, to_update.get(lange, {}))
    # ---
    start_work.work_not_pages()


if __name__ == "__main__":
    main()
