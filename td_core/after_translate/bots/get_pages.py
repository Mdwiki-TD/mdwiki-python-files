#!/usr/bin/python3
"""
from after_translate.bots.get_pages import get_pages_from_db
"""
from newapi import printe

# ---
from mdpy.bots import py_tools
from mdapi_sql import sql_for_mdwiki

# ---
targets_done_by_mdtitle = {}
targets_done = {}
tit_user_lang = {}
langs_to_t_u = {}
to_update = {}
# ---


def get_pages_from_db(lang_o):
    # ---
    sq = sql_for_mdwiki.get_all_pages_all_keys(lang=lang_o)
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
        langs_to_t_u.setdefault(lang, {})
        to_update.setdefault(lang, {})
        to_update[lang].setdefault(user, [])
        # ---
        if not target:
            len_no_target += 1
            # ---
            langs_to_t_u[lang][mdtitle] = user
            # ---
            to_update[lang][user].append(mdtitle)
        else:
            target = target.replace("_", " ")
            target2 = py_tools.ec_de_code(target, "encode")
            # ---
            len_done_target += 1
            # ---
            if lang not in targets_done:
                targets_done[lang] = {}
            # ---
            targets_done[lang][target] = {"user": user, "target": target}
            targets_done[lang][target2] = {"user": user, "target": target}
            # ---
            if lang not in targets_done_by_mdtitle:
                targets_done_by_mdtitle[lang] = {}
            # ---
            targets_done_by_mdtitle[lang][mdtitle] = target
    # ---
    printe.output(f"<<yellow>> find {len_done_target} with target, and {len_no_target} without in mdwiki database. ")
    # ---
    return to_update, langs_to_t_u, targets_done, tit_user_lang, targets_done_by_mdtitle
