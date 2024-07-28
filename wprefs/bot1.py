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
# import os
import sys
from pathlib import Path

# ---
Dir = Path(__file__).parent.parent
# ---
sys.path.append(str(Dir))
# ---
# print(Dir)
# ---
from wprefs.api import GetPageText, page_put
from wprefs.helps import ec_de_code
from wprefs.files import setting, save_wprefcash
from wprefs.wpref_text import fix_page

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


def one_page(page, lang):
    title = ec_de_code(page, "decode")
    # ---
    text = GetPageText(title, lang=lang, Print=False)
    # ---
    if not text:
        print("notext")
        return ""
    # ---
    newtext = fix_page_here(text, title, lang)
    # ---
    if text == newtext:
        print("no changes")
        return ""
    # ---
    if not newtext:
        print("notext")
        return ""
    # ---
    # if "save" in sys.argv:
    #     a = page_put(text, newtext, "Fix references, Expend infobox mdwiki.toolforge.org.", title, lang)
    #     if a:
    #         print("save ok")
    #         return ""
    # ---
    filee = save_wprefcash(title, newtext)
    print(filee)
    # ---
    return ""


def maine():
    # ---
    page = ""
    lange = ""
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        arg = arg[1:] if arg.startswith("-") else arg
        # ---
        if arg == "infobox":
            expend_infobox[1] = True
        if arg == "movedots":
            move_dot[1] = True
        # ---
        if arg == "lang":
            lange = value
        if arg == "page":
            page = value.replace("_", " ")
    # ---
    if page == "" or lange == "":
        print("no page or lang")
        return ""
    # ---
    one_page(page, lange)
    # ---
    return ""


if __name__ == "__main__":
    maine()
