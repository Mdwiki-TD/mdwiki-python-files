"""
this bot get langs from nccommons page:
https://nccommons.org/wiki/User:Mr._Ibrahem/import_bot

"""
import re
from newapi.ncc_page import MainPage as ncc_MainPage
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
    fi = re.findall(r"\* (.*)\n", text)
    for i in fi:
        langs.append(i.strip())
    # ---
    printe.output(f"langs: {langs}")
    return langs
