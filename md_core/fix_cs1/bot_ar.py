"""

python3 core8/pwb.py fix_cs1/bot_ar

tfj run fixcs --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_cs1/bot_ar"

"""
# import re
# import sys

# import wikitextparser as wtp
from newapi import printe
from newapi.page import MainPage, CatDepth, CatDepthLogin

from fix_cs1.fix_p import fix_it


def one_page(title):
    # ---
    page = MainPage(title, "ar", family="wikipedia")
    # ---
    text = page.get_text()
    # ---
    newtext = fix_it(text, site="ar")
    # ---
    if text == newtext:
        return
    # ---
    page.save(newtext=newtext, summary="بوت: إصلاح أخطاء الاستشهاد: دورية مفقودة")


def main():
    CatDepthLogin(sitecode="ar", family="wikipedia")
    # ---
    cat = "تصنيف:أخطاء الاستشهاد: دورية مفقودة"

    cat_members = CatDepth(cat, sitecode="ar", family="wikipedia", depth=0, ns="all")

    for n, page in enumerate(cat_members):
        # ---
        printe.output(f"n: {n}/{len(cat_members)} - Page: {page}")
        one_page(page)


if __name__ == "__main__":
    main()
