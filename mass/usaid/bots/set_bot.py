"""
from mass.eyerounds.bots.set_bot import create_set
"""

import re
import sys
from newapi import printe
# from newapi.ncc_page import CatDepth
from newapi.ncc_page import MainPage as ncc_MainPage

# pages = CatDepth("Category:USAID sets", sitecode="www", family="nccommons", depth=2, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])


def format_text(album_name, files) -> str:
    # files_sorted = sorted(files.items(), key=lambda item: item[1], reverse=True)
    # ---
    files_list = '\n'.join([f"|File:{file_name}|" for _, file_name in files.items()])
    # ---
    text = (
        "{{Imagestack\n"
        "|width=850\n"
        f"|title={album_name}\n"
        "|align=centre\n"
        "|loop=no\n"
        f"{files_list}\n"
        "}}\n"
        "[[Category:Image set]]\n"
        f"[[Category:{album_name}|*]]\n"
        "[[Category:USAID sets|*]]\n"
    )
    # ---
    return text


def create_set(album_name, files) -> bool:
    title = album_name
    # ---
    if "noset" in sys.argv:
        return
    # ---
    title = re.sub(r"[\s_]+", " ", title)
    # ---
    text = format_text(album_name, files)
    # ---
    page = ncc_MainPage(title, "www", family="nccommons")
    # ---
    if not page.exists():
    # if title not in pages or not page.exists():
        ca = page.Create(text=text, summary="Create new set")
        return ca

    printe.output(f"<<lightyellow>>{title} already exists")
    ca = page.save(newtext=text, summary="Update", nocreate=0, minor="")

    return ca
