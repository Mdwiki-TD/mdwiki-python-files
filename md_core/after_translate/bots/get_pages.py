#!/usr/bin/python3
"""
from after_translate.bots.get_pages import get_pages_from_db
"""
from newapi import printe
# ---
from mdpy.bots import py_tools
from mdpy.bots import sql_for_mdwiki
# ---
targets_done = {}
tit_user_lang = {}
langs_to_t_u = {}
to_update = {}
# ---
def get_pages_from_db(lang_o):
    # ---
    que = "select title, user, lang, target from pages "
    # ---
    if lang_o != "":
        langs_to_t_u[lang_o] = {}
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
        else:
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
    return to_update, langs_to_t_u, targets_done, tit_user_lang