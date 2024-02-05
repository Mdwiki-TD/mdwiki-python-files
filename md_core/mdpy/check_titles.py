#!/usr/bin/python3
"""
التحقق من المقالات التحويلات أو المحذوفة

python3 core8/pwb.py mdpy/check_titles test

"""
#
# (C) Ibrahem Qasim, 2024
#
#

import sys
# ---
from newapi import printe
from mdpy.bots import sql_for_mdwiki
from newapi.wiki_page import MainPage, NEW_API
# api_new  = NEW_API('ar', family='wikipedia')

def get_langs_tabs():
    # ---
    que = 'select id, title, lang, target from pages where target != "";'
    # ---
    langs = {}
    # ---
    printe.output(que)
    # ---
    for tab in sql_for_mdwiki.mdwiki_sql(que, return_dict=True):
        lang = tab['lang']
        if not lang in langs:
            langs[lang] = []
        langs[lang].append(tab)
    # ---
    return langs

def get_new_target_log(lang, target):
    # ---
    to_check = target
    # ---
    api_new = NEW_API(lang, family='wikipedia')
    # ---
    printe.output(f'get_new_target_log() lang:{lang}, target:{target}')
    # ---
    while to_check != '':
        logs     = api_new.get_logs(to_check)
        # ---
        new = ''
        # ---
        for log in logs:
            title = log.get("title", "")
            new   = log.get("params", {}).get("target_title", "")
            # ---
            if new:
                break
        # ---
        if new:
            printe.output(f'> title:{to_check} moved to:{new}')
            to_check = new
        else:
            break
    # ---
    printe.output(f'get_new_target_log() lang:{lang}, target:{target}, new:{to_check}')
    # ---
    return to_check

def start():
    # ---
    text = []
    # ---
    langs = get_langs_tabs()
    # ---
    for lang, tabs in langs.items():
        for tab in tabs:
            iid, lang, target = tab["id"], tab["lang"], tab["target"]
            # ---
            new_target = ''
            # ---
            page      = MainPage(target, lang, family='wikipedia')
            # ---
            exists    = page.exists()
            if not exists:
                printe.output(f'page "{target}" not exists in {lang}:{page.family}')
                new_target = get_new_target_log(lang, target)
            elif page.isRedirect() :
                new_target = page.get_redirect_target()
            # ---
            if new_target:
                page2 = MainPage(new_target, lang, family='wikipedia')
                # ---
                if page2.exists() and not page.isRedirect() :
                    printe.output(f'<<yellow>> set_target_where_id() new_target:{new_target}, old target:{target}')
                    text.append([target, lang, new_target])
                    # sql_for_mdwiki.set_target_where_id(new_target, iid)
    # ---
    wikitext = '{|\n|-! target !! lang !! new_target\n|-\n'
    # ---
    for x in text:
        wikitext += f'|-\n| {x[0]} || {x[1]} || {x[2]}\n'
    # ---
    wikitext += '|}'
    # ---
    printe.output(wikitext)

if __name__ == "__main__":
    if 'test' in sys.argv:
        get_new_target_log("ar", "الحكَّة المهبلية")
    else:
        start()