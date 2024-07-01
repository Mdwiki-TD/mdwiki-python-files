"""

python3 core8/pwb.py fix_cs1/bot

tfj run fixcs --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_cs1/bot"

"""
# import re
# import sys

# import wikitextparser as wtp
from newapi import printe
from newapi.mdwiki_page import MainPage as md_MainPage, CatDepth, CatDepthLogin

from fix_cs1.fix_p import fix_it


def one_page(title):
    # ---
    page = md_MainPage(title, "www", family="mdwiki")
    # ---
    text = page.get_text()
    # ---
    newtext = fix_it(text)
    # ---
    if text == newtext:
        return
    # ---
    page.save(newtext=newtext, summary="Fix missing periodical")


def main():
    CatDepthLogin(sitecode="www", family="mdwiki")
    # ---
    cat = "Category:CS1 errors: missing periodical"

    cat_members = CatDepth(cat, sitecode="www", family="mdwiki", depth=0, ns="all")

    for n, page in enumerate(cat_members):
        # ---
        printe.output(f"n: {n}/{len(cat_members)} - Page: {page}")
        one_page(page)


if __name__ == "__main__":
    main()
