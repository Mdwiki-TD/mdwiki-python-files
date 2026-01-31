#!/usr/bin/python3
"""

python3 core8/pwb.py add_rtt/bot
from add_rtt.bot import add_rtt_to_text
# add_rtt_to_text(text, title)


tfj run addrtt1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py add_rtt/bot list"

"""
import logging

# ---
import re
import sys

import wikitextparser as wtp
from add_rtt.named_param import add_param_named
from newapi.mdwiki_page import NEW_API, CatDepth, md_MainPage

logger = logging.getLogger(__name__)

# add_param_named(text, title)

api_new = NEW_API("www", family="mdwiki")
# api_new.Login_to_wiki()


def add_rtt_to_text(text, title):

    new_line = "{{RTT}}"

    if text.find(new_line) != -1:
        logger.info(f"page already tagged.{new_line}")
        return text

    target_templates = ["RTT"]

    parsed = wtp.parse(text)

    for temp in parsed.templates:

        name = str(temp.normal_name()).strip().lower().replace("_", " ")
        if name in target_templates:
            logger.info(f"page already tagged.{title=}")
            return text

    newtext = text

    last_section = None

    for section in parsed.sections:
        last_section = section

    # add line before the first [[Category: in last_section
    if last_section:
        for line in last_section.contents.split("\n"):
            if line.startswith("[[Category:"):
                newtext = newtext.replace(line, f"{new_line}\n{line}")
                break
    else:
        newtext = f"{newtext}\n{new_line}"

    return newtext


def work_page(title):

    page = md_MainPage(title, "www", family="mdwiki")

    if not page.exists():
        return False
    ns = page.namespace()

    if ns != 0:
        return False

    text = page.get_text()
    summary = ""

    newtext = add_rtt_to_text(text, title)

    if newtext != text:
        summary = "Added {{RTT}}"

    newtext2 = add_param_named(newtext, title)

    if newtext2 != newtext:
        summary += ", (|named after=) to Infobox medical condition"
        newtext = newtext2

    save = page.save(newtext=newtext, summary=summary, nocreate=1, minor="")

    return save


def get_list():
    mdwiki_pages = []
    # ---
    title = "WikiProjectMed:WikiProject Medicine/Popular pages"
    page = md_MainPage(title, "www", family="mdwiki")
    # ---
    if not page.exists():
        return []
    # ---
    text = page.get_text()
    # ---
    to_f = "== List =="
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
    mdwiki_pages = [x.strip() for x in mdwiki_pages if x.find("|") == -1]
    # ---
    mdwiki_pages.sort()
    # ---
    logger.info(f"len of mdwiki_pages: {len(mdwiki_pages)}")
    # ---
    return mdwiki_pages


def get_titles():
    # ---
    mdwiki_pages = []
    # ---
    if "list" in sys.argv:
        mdwiki_pages = get_list()
        # ---
    else:
        mdwiki_pages = CatDepth("Category:RTT", sitecode="www", family="mdwiki", depth=0, ns=0)
    # ---
    return mdwiki_pages


def main():

    mdwiki_pages = get_titles()

    temp_pages = api_new.Get_template_pages("Template:RTT", namespace=0)

    logger.info(f"len of mdwiki_pages: {len(mdwiki_pages)}, temp_pages: {len(temp_pages)}")

    # pages in mdwiki_pages but not in temp_pages
    pages_to_add = [x for x in mdwiki_pages if x not in temp_pages]

    logger.info(f"len of pages_to_add: {len(pages_to_add)}")

    for x in pages_to_add:
        work_page(x)


if __name__ == "__main__":
    main()
