"""
this bot get langs from nccommons page:
https://nccommons.org/wiki/User:Mr._Ibrahem/import_bot

"""
# import re
import wikitextparser as wtp
from nc_import.api_bots.ncc_page import ncc_MainPage
from newapi import printe


def get_text():
    """
    Retrieves text content from a specific page.
    """
    title = "User:Mr. Ibrahem/import bot"
    page = ncc_MainPage(title, "www", family="nccommons")
    text = page.get_text()
    # match all langs like: * ar\n* fr
    # ---
    return text


def get_langs_codes():
    """
    Extracts language codes from the text content of a page.
    """
    text = get_text()
    langs = []
    # * {{User:Mr. Ibrahem/import bot/line|ar}}
    # ---
    tmp = "User:Mr. Ibrahem/import bot/line"
    # ---
    prased = wtp.parse(text)
    temps = prased.templates
    for temp in temps:
        # ---
        name = str(temp.normal_name()).strip().lower().replace("_", " ")
        # ---
        printe.output(f"{temp.name=}, {name=}")
        # ---
        if name == tmp.lower():
            # ---
            # get first argument
            # ---
            va = temp.get_arg("1")
            if va and va.value:
                langs.append(va.value.strip())
    # ---
    printe.output(f"langs: {langs}")
    # ---
    return langs


if __name__ == "__main__":
    # python3 core8/pwb.py nc_import/bots/get_langs
    get_langs_codes()
