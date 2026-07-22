#!/usr/bin/python3
"""

python3 core8/pwb.py md_core/add_rtt/bot

"""

import logging

import wikitextparser as wtp

from mdwiki_api.mdwiki_page import CatDepth, NewApi, md_MainPage

logger = logging.getLogger(__name__)
api_new = NewApi("www", family="mdwiki")


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

        save = page.save(newtext=newtext, summary=summary, nocreate=1, minor="")

        return save

    return False


def main():
    mdwiki_pages = CatDepth("Category:RTT", sitecode="www", family="mdwiki", depth=0, ns=0)
    temp_pages = api_new.Get_template_pages("Template:RTT", namespace=0)

    logger.info(f"len of mdwiki_pages: {len(mdwiki_pages)}, temp_pages: {len(temp_pages)}")

    pages_to_add = [x for x in mdwiki_pages if x not in temp_pages]

    logger.info(f"len of pages_to_add: {len(pages_to_add)}")

    for x in pages_to_add:
        work_page(x)


if __name__ == "__main__":
    main()
