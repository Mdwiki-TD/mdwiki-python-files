#!/usr/bin/python3
"""

python3 core8/pwb.py add_rtt/bot
from add_rtt.bot import add_rtt_to_text
# add_rtt_to_text(text, title)


"""
# ---
import wikitextparser as wtp

from newapi import printe
from newapi.mdwiki_page import NEW_API, md_MainPage, CatDepth

from add_rtt.named_param import add_param_named
# add_param_named(text, title)


api_new = NEW_API("www", family="mdwiki")
# api_new.Login_to_wiki()


def add_rtt_to_text(text, title):
    target_templates = [
        "RTT"
    ]

    parsed = wtp.parse(text)

    for temp in parsed.templates:

        name = str(temp.normal_name()).strip().lower().replace("_", " ")
        if name in target_templates:
            printe.output(f"page already tagged.{title=}")
            return text

    new_line = "{{RTT}}"

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


def main():

    mdwiki_pages = CatDepth("Category:RTT", sitecode="www", family="mdwiki", depth=0, ns=0)

    temp_pages = api_new.Get_template_pages("Template:RTT", namespace=0)

    printe.output(f"len of mdwiki_pages: {len(mdwiki_pages)}, temp_pages: {len(temp_pages)}")

    # pages in mdwiki_pages but not in temp_pages
    pages_to_add = [x for x in mdwiki_pages if x not in temp_pages]

    printe.output(f"len of pages_to_add: {len(pages_to_add)}")

    for x in pages_to_add:
        work_page(x)


if __name__ == "__main__":
    main()
