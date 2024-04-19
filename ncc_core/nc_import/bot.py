"""

python3 core8/pwb.py nc_import/bot ask

"""
import sys
from nc_import.bots.gt_pages import get_pages
from nc_import.bots.wrk_pages import work_on_pages
from nc_import.bots.get_langs import get_langs_codes


def start():
    """
    A function that starts the process by iterating over languages, getting pages for each language, and then working on those pages.
    """
    lang = ""
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg == "-lang":
            lang = value
    # ---
    langs = get_langs_codes()
    # ---
    if lang and lang in langs:
        langs = [lang]
    # ---
    for code in langs:
        pages = get_pages(code)
        work_on_pages(code, pages)


if __name__ == "__main__":
    start()
