#!/usr/bin/python3
"""

python3 core8/pwb.py add_rtt/remove

"""
# ---

import logging

from mdwiki_api.mdwiki_page import NEW_API, CatDepth, md_MainPage

logger = logging.getLogger(__name__)

# add_param_named(text, title)

api_new = NEW_API("www", family="mdwiki")


def work_page(title):

    page = md_MainPage(title, "www", family="mdwiki")

    if not page.exists():
        return False
    ns = page.namespace()

    if ns != 0:
        return False

    text = page.get_text()
    summary = ""
    if text.find("[[Category:RTT") != -1:
        return

    newtext = text.replace("{{RTT}}", "")

    if newtext != text:
        page.save(newtext=newtext, summary=summary, nocreate=1, minor="")


def main():
    mdwiki_pages = CatDepth("Category:RTT", sitecode="www", family="mdwiki", depth=0, ns=0)
    # ---
    temp_pages = api_new.Get_template_pages("Template:RTT", namespace=0)
    logger.info(f"len of mdwiki_pages: {len(mdwiki_pages)}, temp_pages: {len(temp_pages)}")
    pages_to_remoe = [x for x in temp_pages if x not in mdwiki_pages]

    logger.info(f"len of pages_to_remoe: {len(pages_to_remoe)}")

    for x in pages_to_remoe:
        work_page(x)


if __name__ == "__main__":
    main()
