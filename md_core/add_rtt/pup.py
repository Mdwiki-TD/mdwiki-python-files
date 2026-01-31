#!/usr/bin/python3
"""

python3 core8/pwb.py add_rtt/pup
from add_rtt.bot import add_rtt_to_text
# add_rtt_to_text(text, title)


tfj run addrtt1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py add_rtt/pup"

https://github.com/wikimedia/popularpages

"""
import logging
import re

# ---
import sys
from pathlib import Path

import wikitextparser as wtp
from add_rtt.r_column_bots.pup_table import R_NEW_ROW, add_to_tables, fix_title
from newapi.mdwiki_page import NEW_API, md_MainPage  # , CatDepth

logger = logging.getLogger(__name__)

Dir = Path(__file__).parent
# add_param_named(text, title)

api_new = NEW_API("www", family="mdwiki")
# api_new.Login_to_wiki()


def find_redirects(pages, text):
    # ---
    to_f = "== List =="
    # ---
    mdwiki_pages = []
    # ---
    if text.find(to_f) != -1:
        text = text.split(to_f)[1]
        # match all links like [[.*?]]
        pattern = r"\[\[(.*?)\]\]"
        links = re.findall(pattern, text)
        mdwiki_pages = links
    # ---
    mdwiki_pages = list(set(mdwiki_pages))
    # ---
    mdwiki_pages = [fix_title(x.strip()) for x in mdwiki_pages if x.find("|") == -1 and x not in pages]
    # ---
    logger.info(f" pages: {len(mdwiki_pages)}")
    # ---
    titles = api_new.get_titles_redirects(mdwiki_pages)
    # ---
    # titles = api_new.get_titles_redirects(["Ehlers–Danlos syndrome"]) # {'Ehlers–Danlos syndrome': 'Ehlers–Danlos syndromes'}
    redirects = {x: y for x, y in titles.items()}
    # ---
    return redirects


def work_page():
    title = "WikiProjectMed:WikiProject Medicine/Popular pages"
    page = md_MainPage(title, "www", family="mdwiki")

    if not page.exists():
        return False

    text = page.get_text()

    new_text = add_to_tables(text)

    if new_text != text:
        page.save(newtext=new_text, summary="Add R column")
        text = new_text
    # ---
    if "only_column" in sys.argv:
        return
    # ---
    old_counts = text.count(R_NEW_ROW.strip())
    # ---
    # pages = CatDepth("Category:RTT", sitecode="www", family="mdwiki", depth=0, ns=0)
    pages = api_new.Get_template_pages("Template:RTT", namespace=0)

    redirects = find_redirects(pages, text)

    newtext = add_to_tables(text, redirects, pages)

    with open(Dir / "page_text.txt", "w", encoding="utf-8") as f:
        f.write(newtext)

    if newtext == text:
        logger.info("no changes")
        return False

    # count R_NEW_ROW in newtext
    counts = newtext.count(R_NEW_ROW.strip())

    counts = counts - old_counts

    summary = f"Added R column to {counts} titles."

    page.save(newtext=newtext, summary=summary, nocreate=1, minor="")


def main():

    work_page()


if __name__ == "__main__":
    main()
