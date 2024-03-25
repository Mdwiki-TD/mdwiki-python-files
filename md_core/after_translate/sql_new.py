#!/usr/bin/python3
"""
بوت قواعد البيانات

python3 core8/pwb.py after_translate/sql_new
python3 core8/pwb.py after_translate/sql_new pages_users
python3 core8/pwb.py after_translate/sql_new justsql break
python3 core8/pwb.py after_translate/sql_new justsql
python3 core8/pwb.py after_translate/sql_new -lang:ur

"""

#
# (C) Ibrahem Qasim, 2024
#
#
import re
import sys
import time

from after_translate.bots import add_to_wd
from after_translate.bots.add_to_mdwiki import add_to_mdwiki_sql
from after_translate.bots.fixcat import cat_for_pages
from after_translate.bots.get_pages import get_pages_from_db

# ---
from after_translate.bots.users_pages import not_pages
from api_sql import wiki_sql

# ---
from mdpy.bots import py_tools

# ---
from newapi import printe

# ---
skip_langs = ["zh-yue", "ceb"]
# ---
titles_not_0 = []
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
        # AND r.rev_parent_id = 0
        # AND r.rev_timestamp > 20210101000000
        AND r.rev_timestamp > 20240101000000
        AND comment_text like "%User:Mr. Ibrahem/%" #AND p.page_namespace = 0
    GROUP BY
        p.page_title,
        a.actor_name,
        c.comment_text
    """


def start(result, lange, tgd, tgd_by_md, tit_user_lang):
    printe.output(f'sql.py len(result) = "{len( result )}"')
    # ---
    tab_lang = {}
    # ---
    to_add = 0
    done = 0
    # ---
    for lis in result:
        # ---
        done += 1
        # ---
        target = lis["title"]
        co_text = lis["comment_text"]
        user = lis["actor_name"]
        pupdate = lis["rev_timestamp"]
        ns = str(lis["page_namespace"])
        # ---
        pupdate = pupdate[:8]
        pupdate = re.sub(r"^(\d\d\d\d)(\d\d)(\d\d)$", r"\g<1>-\g<2>-\g<3>", pupdate)
        # ---
        md_title = co_text.replace("_", " ").strip()
        md_title = re.sub("/full$", "", co_text)
        # ---
        target = target.replace("_", " ")
        # ---
        target = f"user:{target}" if ns == "2" else target
        # ---
        user = user.replace("_", " ")
        # ---
        # tgd_by_md
        target_in = tgd_by_md.get(md_title, "")
        # ---
        laox = f"<<yellow>>{md_title=},    <<yellow>>{user=},    <<yellow>>{ns=}, {lange=}:{target.ljust(20)=},   <<yellow>>{pupdate=}"
        # ---
        if ns != "0" and target_in != target:
            laox += f", <<purple>>[[{target_in=}]]"
        # ---
        if "print" in sys.argv:
            printe.output(laox)
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
        target2 = py_tools.ec_de_code(target, "encode")
        # ---
        tul = md_title + user + lange
        tul_target = tit_user_lang.get(tul, "")
        # ---
        cattest = cat_for_pages.get(md_title, "")
        # ---
        # if ns != "0":
        if target_in != "" and target_in != target:
            if "ns" in sys.argv and tul_target == "" and cattest:
                printe.output(laox)
            continue
        # ---
        not_puplished = target2 not in tgd and target not in tgd
        # ---
        # للتأكد من الصفحات غير المنشورة
        if not_puplished and target_in == "":
            # ---
            if tul_target == "":
                printe.output(laox)
                to_add += 1
                tab_lang[md_title] = Taba2
                # ---
                if ns != "0":
                    titles_not_0.append(Taba2)

            elif tul_target == target:
                printe.output(f"target already in, {target}")

            else:
                printe.output(f"puplished target: {tul_target} != target to add: {target}")
    # ---
    printe.output(f"lang: {lange} done: {done}, to_add: {to_add}")
    # ---
    return tab_lang


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
    to_update, langs_to_t_u, targets_done, tit_user_lang, targets_done_by_mdtitle = get_pages_from_db(lang_o)
    # ---
    time.sleep(3)
    # ---
    numb_lang = 0
    lnn = len(langs_to_t_u.keys())
    # ---
    for lange in langs_to_t_u:
        # ---
        # tab_by_lang[lange] = {}
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
        if result == {}:
            printe.output("no result")
            continue
        # ---
        lang_tab = start(result, lange, tgd, tgd_by_md, tit_user_lang)
        # ---
        if "only" in sys.argv:
            continue
        # ---
        if "justsql" not in sys.argv:
            add_to_wd.add_tab_to_wd({lange: lang_tab})
        # ---
        add_to_mdwiki_sql({lange: lang_tab}, to_update.get(lange, {}))
    # ---
    not_pages(titles_not_0)


if __name__ == "__main__":
    main()
