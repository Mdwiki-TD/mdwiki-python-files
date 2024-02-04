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
from after_translate.bots import add_to_wd
from after_translate.bots.add_to_mdwiki import add_to_mdwiki_sql
from after_translate.bots.fixcat import cat_for_pages

# ---
from mdpy.bots import py_tools
from mdpy.bots import sql_for_mdwiki
from api_sql import wiki_sql
# ---
targets_done = {}
langs_to_t_u = {}
to_update = {}
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
tit_user_lang = {}
# ---
query_main_old = """
    select DISTINCT p.page_title, c.comment_text , a.actor_name , r.rev_timestamp
    from change_tag t
    INNER JOIN change_tag_def ctd on ctd.ctd_id = t.ct_tag_id
    INNER JOIN revision r on r.rev_id = t.ct_rev_id
    INNER JOIN actor a ON r.rev_actor = a.actor_id
    inner join comment c on c.comment_id = r.rev_comment_id
    INNER JOIN page p on r.rev_page=p.page_id
    where ctd.ctd_name in ("contenttranslation", "contenttranslation-v2") #id = 3 # id = 120
    and r.rev_parent_id = 0
    #AND a.actor_name in ('Mr. Ibrahem')
    AND r.rev_timestamp > 20210101000000
    #and comment_text like "%[[:en:Special:Redirect/revision/%|User:Mr. Ibrahem/%]]%"
    and comment_text like "%User:Mr. Ibrahem/%"
    and p.page_namespace = 0
    #limit 10
"""
# ---
query_main = """
    select DISTINCT p.page_title as title,
    SUBSTRING_INDEX(SUBSTRING_INDEX(c.comment_text, 'Ibrahem/', -1), ']]', 1) as comment_text,
    a.actor_name, r.rev_timestamp, p.page_namespace, r.rev_parent_id
    from change_tag t
    INNER JOIN change_tag_def ctd on ctd.ctd_id = t.ct_tag_id
    INNER JOIN revision r on r.rev_id = t.ct_rev_id
    INNER JOIN actor a ON r.rev_actor = a.actor_id
    inner join comment c on c.comment_id = r.rev_comment_id
    INNER JOIN page p on r.rev_page=p.page_id
    where ctd.ctd_name in ("contenttranslation", "contenttranslation-v2") #id = 3 # id = 120
    #and r.rev_parent_id = 0
    AND r.rev_timestamp > 20210101000000
    and comment_text like "%User:Mr. Ibrahem/%"
    #and p.page_namespace = 0
    group by p.page_title, a.actor_name, c.comment_text
"""


def get_pages_from_db():
    # ---
    lang_o = ""
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg in ["lang", "-lang"]:
            lang_o = value
            langs_to_t_u[value] = {}
        # ---
    # ---
    que = "select title, user, lang, target from pages "
    # ---
    if lang_o != "":
        que += f' where lang = "{lang_o}"'
    # ---
    que += " ;"
    # ---
    printe.output(que)
    # ---
    sq = sql_for_mdwiki.mdwiki_sql(que, return_dict=True)
    # ---
    len_no_target = 0
    len_done_target = 0
    # ---
    for tab in sq:
        mdtitle = tab["title"]
        user = tab["user"]
        target = tab["target"]
        lang = tab["lang"].lower()
        # ---
        if lang_o != "" and lang != lang_o.strip():
            continue
        # ---
        tul = mdtitle + user + lang
        tit_user_lang[tul] = target
        # ---
        if lang not in langs_to_t_u:
            langs_to_t_u[lang] = {}
        # ---
        if lang not in to_update:
            to_update[lang] = {}
        # ---
        if user not in to_update[lang]:
            to_update[lang][user] = []
        # ---
        if target == "":
            len_no_target += 1
            # ---
            langs_to_t_u[lang][mdtitle] = user
            # ---
            to_update[lang][user].append(mdtitle)
            # ---
        else:
            # ---
            if lang not in targets_done:
                targets_done[lang] = {}
            # ---
            target = target.replace("_", " ")
            target2 = py_tools.ec_de_code(target, "encode")
            # ---
            len_done_target += 1
            # ---
            targets_done[lang][target] = {"user": user, "target": target}
            targets_done[lang][target2] = {"user": user, "target": target}
    # ---
    printe.output(f"<<lightyellow>> find {len_done_target} with target, and {len_no_target} without in mdwiki database. ")
    # ---
    if "print" in sys.argv:
        printe.output(langs_to_t_u)
    # ---
    time.sleep(3)


def start(result, lange):
    printe.output(f'sql.py len(result) = "{len( result )}"')
    # ---
    # texddt = '\n'
    # ---
    for lis in result:
        # ---
        # printe.output( lis )
        # ---
        target = lis["title"]
        co_text = lis["comment_text"]
        user = lis["actor_name"]
        pupdate = lis["rev_timestamp"]
        namespace = lis["page_namespace"]
        # rev_parent_id = lis['rev_parent_id']
        # ---
        namespace = str(namespace)
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
            "namespace": namespace,
        }
        # ---
        laox = f"<<lightyellow>> target:{lange}:{target.ljust(40)}, ns:{namespace.ljust(3)} for mdtit:<<lightyellow>>{md_title.ljust(30)}, user:<<lightyellow>>{user}"
        # ---
        tgd = targets_done.get(lange, {})
        # ---
        target2 = py_tools.ec_de_code(target, "encode")
        # ---
        tul = md_title + user + lange
        tul_target = tit_user_lang.get(tul, "")
        # ---
        cattest = cat_for_pages.get(md_title, "")
        # ---
        if namespace != "0":
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
                printe.output(
                    f"puplished target: {tul_target} != target to add: {target}"
                )


def main():
    # ---
    get_pages_from_db()
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
        result = {}
        # ---
        qua = query_main
        # ---
        if lange == "ar":
            qua += """
                and p.page_title not in (
                    'جامعة_نورث_كارولاينا',
                    'جامعة_ولاية_كارولينا_الشمالية_إيه_آند_تي',
                    'نيشان_راجاميترابورن'
                )
            """
        # ---
        qua += "\n;"
        # ---
        if lange in skip_langs:
            printe.output(f"skip lang:{lange}")
            continue
        # ---
        if "printquery" in sys.argv:
            print(qua)
        # ---
        result = wiki_sql.sql_new(qua, str(lange))
        # ---
        if result != {}:
            start(result, lange)
        # ---
        add_to_wd.add_tab_to_wd({lange: tab_by_lang[lange]})
        # ---
        add_to_mdwiki_sql({lange: tab_by_lang[lange]}, to_update)


if __name__ == "__main__":
    main()
