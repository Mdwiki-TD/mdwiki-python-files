#!/usr/bin/python3
"""

تجميع المراجع في الصفحات

python3 core8/pwb.py wprefs/bot -lang:es ask savetofile
python3 core8/pwb.py wprefs/bot -lang:or ask -page:ପାଟେଲୋଫିମୋରାଲ_ଯନ୍ତ୍ରଣା_ସିଣ୍ଡ୍ରୋମ
python3 core8/pwb.py wprefs/bot -lang:or ask -page:ପୋଷ୍ଟିରିଅର_ୟୁରେଥ୍ରାଲ_ଭଲଭ ask
python3 core8/pwb.py wprefs/bot -lang:or -page:user:Mr._Ibrahem/sandbox ask

python3 core8/pwb.py wprefs/bot -lang:ro ask

python3 core8/pwb.py wprefs/bot ask

"""
#
# (C) Ibrahem Qasim, 2023
#
#
import sys
from mdapi_sql import sql_for_mdwiki

# ---
from wprefs.api import log, GetPageText, GetPageText_raw, missingtitles, page_put
from wprefs.files import reffixed_list, setting, append_reffixed_file
from wprefs.wpref_text import fix_page
from newapi import printe

skip_langs = ["en"]
move_dot = {1: False}
expend_infobox = {1: False}


def fix_page_here(text, title, langcode):
    newtext = text
    # ---
    section_0_text = ""
    # ---
    lang_default = setting.get(langcode, {})
    # ---
    dots = move_dot[1]
    if lang_default.get("move_dots", 0) == 1:
        dots = True
    # ---
    expend = expend_infobox[1]
    if lang_default.get("expend", 0) == 1:
        expend = True
    # ---
    adden = False
    if lang_default.get("add_en_lang", 0) == 1:
        adden = True
    # ---
    newtext = fix_page(newtext, title, move_dots=dots, infobox=expend, section_0=section_0_text, lang=langcode, add_en_lang=adden)
    # ---
    return newtext


def work_one_lang(list_, lang):
    # ---
    printe.output(f"<<blue>> work on lang: {lang}.wikipedia......................")
    # ---
    if lang in skip_langs:
        printe.output(f"<<blue>> skip lang: {lang}.wikipedia......................")
        return
    # ---
    newlist = list_
    # ---
    if "lala" not in sys.argv:
        newlist = [x for x in list_ if f"{lang}:{x}" not in reffixed_list]
        dd = int(len(list_)) - int(len(newlist))
        print(f"already in reffixed_list :{dd}")
    # ---
    # if len(newlist) > 0: log(lang)
    # ---
    number = 0
    # ---
    dns = []
    # ---
    for title in newlist:
        # ---
        lio = f"{lang}:{title}"
        number += 1
        printe.output(f"<<yellow>> {number} from {len(newlist)}, page: {lio}")
        # ---
        if lio in reffixed_list and "lala" not in sys.argv:
            printe.output("<<red>>\talready in reffixed_list.")
            continue
        # ---
        if "adddone" in sys.argv:
            dns.append(title)
            continue
        # ---
        text = GetPageText_raw(title, lang=lang)
        # ---
        if not text:
            printe.output('\ttext == ""')
            continue
        # ---
        newtext = fix_page_here(text, title, lang)
        # ---
        donee = False
        # ---
        if text != newtext:
            aa = page_put(text, newtext, "Fix references, Expand infobox #mdwiki .toolforge.org.", title, lang)
            # ---
            if aa:
                donee = True
        # ---
        if donee or "donee" in sys.argv:
            append_reffixed_file(lang, title)
    # ---
    if dns:
        append_reffixed_file(lang, "", dns)


def work_sql_result(lange, nolange, year=2024):
    newtable = {}
    que = f"""
        select lang, target from pages
        where target != ""
        and lang != ""
        and lang != "ar"
        and date like "{year}-%"
        ;
    """
    # ---
    if nolange != "":
        que = que.replace('and lang != ""', f'and lang != "{nolange}"')
    elif lange != "":
        que = f'select lang, target from pages where target != "" and lang = "{lange}" and date like "{year}-%";'
    # ---
    printe.output(que)
    # ---
    sq = sql_for_mdwiki.mdwiki_sql(que, return_dict=True)
    # ---
    for tab in sq:
        lang = tab["lang"]
        target = tab["target"]
        # ---
        if lang not in newtable:
            newtable[lang] = []
        if target not in newtable[lang]:
            newtable[lang].append(target)
    return newtable


def maine():
    # ---
    lange = ""
    nolange = ""
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        # ---
        arg = arg[1:] if arg.startswith("-") else arg
        # ---
        if arg == "infobox":
            expend_infobox[1] = True
        # ---
        if arg == "movedots":
            move_dot[1] = True
        # ---
        if arg == "nolang":
            nolange = value
        # ---
        if arg == "lang":
            lange = value
    # ---
    newtable = work_sql_result(lange, nolange)
    # ---
    for lang, tab in newtable.items():
        work_one_lang(tab, lang)
    # ---
    printe.output(f"find {len(missingtitles)} pages in missingtitles")
    # ---
    for x, lang in missingtitles.items():
        printe.output(f"lang: {lang}, title: {x}")


if __name__ == "__main__":
    maine()
