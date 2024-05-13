"""
from mass.eyerounds.bots.set_bot import create_set
"""

import sys
from newapi import printe
from newapi.ncc_page import CatDepth
from newapi.ncc_page import MainPage as ncc_MainPage

pages = CatDepth("Category:EyeRounds sets", sitecode="www", family="nccommons", depth=2, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])


def create_set(chapter_name, files):
    title = chapter_name
    # ---
    if "noset" in sys.argv:
        return
    # ---
    title = title.replace("_", " ").replace("  ", " ")
    text = "" + "{{Imagestack\n|width=850\n"
    text += f"|title={chapter_name}\n|align=centre\n|loop=no\n"
    # ---
    for file_name in files:
        text += f"|File:{file_name}|\n"
    # ---
    text += "\n}}\n[[Category:Image set]]\n"
    text += f"[[Category:{chapter_name}|*]]"
    # ---
    page = ncc_MainPage(title, "www", family="nccommons")
    if title not in pages:
        ca = page.Create(text=text, summary="")
    else:
        printe.output(f"<<lightyellow>>{title} already exists")
        ca = page.save(newtext=text, summary="update", nocreate=0, minor="")

    return ca
