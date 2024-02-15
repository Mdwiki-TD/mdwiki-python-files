#!/usr/bin/python3
"""
بوت قواعد البيانات

python3 core8/pwb.py after_translate/sql justsql break
python3 core8/pwb.py after_translate/sql justsql
python3 core8/pwb.py after_translate/sql

"""

#
# (C) Ibrahem Qasim, 2024
#
#
import re
import sys
import time

# ---
from newapi import printe

# ---
from after_translate.bots.get_pages import get_pages_from_db
from after_translate.bots import add_to_wd
from after_translate.bots.add_to_mdwiki import add_to_mdwiki_sql
from after_translate.bots.fixcat import cat_for_pages

# ---
from mdpy.bots import py_tools
from mdpy.bots import sql_for_mdwiki
from api_sql import wiki_sql
# ---
skip_langs = ["zh-yue", "ceb"]
# ---
tab_by_lang = {}
# ---
Skip_titles = {
    "Mr. Ibrahem": {
        "targets": [
            "جامعة نورث كارولاينا",
            "جامعة ولاية كارولينا الشمالية إيه آند تي",
            "نيشان راجاميترابورن",
        ],
        "mdtitles": [],
    },
    "Avicenno": {
        "targets": ["ألم فرجي", "لقاح المكورة السحائية", "استئصال اللوزتين"],
        "mdtitles": [],
    },
    "Subas Chandra Rout": {
        "targets": [],
        "mdtitles": [
            "Wilms' tumor",
            "Sheehan's syndrome",
            "Membranous nephropathy",
        ],
    },
}
# ---
Skip_titles_global = [
    "جامعة نورث كارولاينا",
    "جامعة ولاية كارولينا الشمالية إيه آند تي",
    "نيشان راجاميترابورن",
    "موميتازون",
]
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
        #AND r.rev_parent_id = 0 # AND r.rev_timestamp > 20210101000000
        AND r.rev_timestamp > 20240101000000
        AND comment_text like "%User:Mr. Ibrahem/%" #AND p.page_namespace = 0
    GROUP BY
        p.page_title,
        a.actor_name,
        c.comment_text
    """


def start(result, lange, tgd, tit_user_lang):
    printe.output(f'sql.py len(result) = "{len( result )}"')
    # ---
    for lis in result:
        # ---
        target  = lis["title"]
        co_text = lis["comment_text"]
        user    = lis["actor_name"]
        pupdate = lis["rev_timestamp"]
        ns      = str(lis["page_namespace"])
        # ---
        pupdate = pupdate[:8]
        pupdate = re.sub(r"^(\d\d\d\d)(\d\d)(\d\d)$", r"\g<1>-\g<2>-\g<3>", pupdate)
        # ---
        md_title = co_text.replace("_", " ").strip()
        md_title = re.sub("/full$", "", co_text)
        # ---
        target = target.replace("_", " ")
        # ---
        user = user.replace("_", " ")
        # ---
        if target in Skip_titles_global:
            continue
        if target in Skip_titles.get(user, {}).get("targets", []):
            continue
        # ---
        if md_title in Skip_titles.get(user, {}).get("mdtitles", []):
            continue
        # ---
        Taba2 = {
            "mdtitle": md_title,
            "target": target,
            "user": user,
            "lang": lange,
            "pupdate": pupdate,
            "namespace": ns,
        }
        # ---
        laox = f"<<lightyellow>> target:{lange}:{target.ljust(40)}, ns:{ns.ljust(3)} for mdtit:<<lightyellow>>{md_title.ljust(30)}, user:<<lightyellow>>{user}"
        # ---
        target2 = py_tools.ec_de_code(target, "encode")
        # ---
        tul = md_title + user + lange
        tul_target = tit_user_lang.get(tul, "")
        # ---
        cattest = cat_for_pages.get(md_title, "")
        # ---
        if ns != "0":
            if "ns" in sys.argv and tul_target == "" and cattest:
                printe.output(laox)
            continue
        # ---
        # للتأكد من الصفحات غير المنشورة
        if target2 not in tgd and target not in tgd:
            # ---
            if tul_target == "":
                tab_by_lang[lange][md_title] = Taba2
                printe.output(laox)
            elif tul_target == target:
                printe.output(f"target already in, {target}")
            else:
                printe.output(f"puplished target: {tul_target} != target to add: {target}")


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
    # ---
    to_update, langs_to_t_u, targets_done, tit_user_lang = get_pages_from_db(lang_o)
    # ---
    time.sleep(3)
    # ---
    numb_lang = 0
    lnn = len(langs_to_t_u.keys())
    # ---
    for lange in langs_to_t_u:
        # ---
        tab_by_lang[lange] = {}
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
        # ---
        if result != {}:
            start(result, lange, tgd, tit_user_lang)
        # ---
        add_to_wd.add_tab_to_wd({lange: tab_by_lang[lange]})
        # ---
        add_to_mdwiki_sql({lange: tab_by_lang[lange]}, to_update)


if __name__ == "__main__":
    main()
