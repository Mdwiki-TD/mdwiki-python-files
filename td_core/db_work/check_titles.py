#!/usr/bin/python3
"""

التحقق من المقالات التحويلات أو المحذوفة في الويكيات

python3 core8/pwb.py db_work/check_titles -lang:ur

python3 core8/pwb.py db_work/check_titles test

"""
import sys
import time

import tqdm
from db_work.check_titles_helps import Find_pages_exists, WikiPage, get_new_target_log
from mdapi_sql import sql_for_mdwiki

# ---
from newapi import printe
from newapi.mdwiki_page import md_MainPage

skip_by_lang = {
    "ar": ["الأنسولين"],
}


def get_langs_tabs():
    # ---
    que = 'select id, title, lang, target from pages where target != "";'
    # ---
    lang_to_get = ""
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg == "-lang":
            lang_to_get = value
    # ---
    langs = {}
    # ---
    printe.output(que)
    # ---
    for tab in sql_for_mdwiki.select_md_sql(que, return_dict=True):
        lang = tab["lang"]
        if lang not in langs:
            langs[lang] = []
        langs[lang].append(tab)
    # ---
    if lang_to_get in langs:
        langs = {lang_to_get: langs[lang_to_get]}
    # ---
    return langs


def add_text(tab):
    # ---
    if not tab:
        return
    # ---
    date = time.strftime("%Y-%m-%d", time.gmtime())
    # ---
    wikitext = f"== {date} ==\n"
    wikitext += "{|\n|-\n! lang !! target !! new_target\n|-\n"
    # ---
    for x in tab:
        wikitext += f"|-\n| {x[0]} || [[:{x[0]}:{x[1]}]] || [[:{x[0]}:{x[2]}]]\n"
    # ---
    wikitext += "|}\n"
    # ---
    printe.output(wikitext)
    itle = "User:Mr. Ibrahem/tofix"
    # ---
    page = md_MainPage(itle, "www", family="mdwiki")
    # ---
    text = page.get_text()
    newtext = f"{wikitext}\n{text}"
    # ---
    page.save(newtext=newtext, summary="update", nocreate=0)


def start():
    # ---
    deleted_pages = []
    to_set = {}
    text = []
    # ---
    langs = get_langs_tabs()
    # ---
    for lang, tabs in langs.items():
        # ---
        printe.output(f"<<green>> lang:{lang}, has {len(tabs)} tabs")
        # ---
        titles = [x["target"] for x in tabs]
        # ---
        pages = Find_pages_exists(lang, titles)
        # ---
        missing = [x for x, v in pages.items() if not v]
        redirects = [x for x, v in pages.items() if v == "redirect"]
        # ---
        printe.output(f"lang:{lang}, missing:{len(missing)}, redirects:{len(redirects)}")
        # ---
        new_tabs = [tab for tab in tabs if tab["target"] in missing or tab["target"] in redirects]
        # ---
        printe.output(f"lang:{lang}, has {len(new_tabs)} new tabs")
        # ---
        for tab in tqdm.tqdm(new_tabs):
            iid, lang, target = tab["id"], tab["lang"], tab["target"]
            # ---
            skip_it = skip_by_lang.get(lang, {})
            # ---
            if target in skip_it:
                printe.output(f"<<yellow>> skip {target}")
                continue
            # ---
            new_target = ""
            # ---
            if target in missing and "onlyredirect" not in sys.argv:
                printe.output(f'<<red>> page "{target}" not exists in {lang}')
                deleted, new_target = get_new_target_log(lang, target)
                if deleted:
                    printe.output(f'<<red>> page "{target}" deleted in {lang}')
                    deleted_pages.append(iid)
                # ---
            elif target in redirects:
                page = WikiPage(target, lang, family="wikipedia")
                new_target = page.get_redirect_target()
            # ---
            if new_target:
                page2 = WikiPage(new_target, lang, family="wikipedia")
                # ---
                if page2.exists():
                    if page2.isRedirect():
                        printe.output(f"<<yellow>> set_target_where_id() new_target:{new_target}, old target:{target}")
                        # ---
                        to_set[iid] = new_target
                        # sql_for_mdwiki.set_target_where_id(new_target, iid)
                        # ---
                        text.append([lang, target, new_target])
                # else:
                #     printe.output(f'<<red>> page "{new_target}" deleted from {lang}')
                #     deleted.append(iid)
    # ---
    printe.output(f"len of to_set {len(to_set)}")
    # ---
    for iid, new_target in to_set.items():
        printe.output(f"<<green>> set_target_where_id() new_target:{new_target}, old iid:{iid}")
        if "test" not in sys.argv:
            sql_for_mdwiki.set_target_where_id(new_target, iid)
    # ---
    printe.output(f"len of deleted_pages {len(deleted_pages)}")
    printe.output(f"len of text {len(text)}")
    # ---
    if "test" not in sys.argv:
        for iid in deleted_pages:
            sql_for_mdwiki.set_deleted_where_id(iid)
        # ---
        if text:
            add_text(text)


if __name__ == "__main__":
    start()
