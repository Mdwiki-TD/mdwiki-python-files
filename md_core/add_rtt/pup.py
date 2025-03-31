#!/usr/bin/python3
"""

python3 core8/pwb.py add_rtt/bot
from add_rtt.bot import add_rtt_to_text
# add_rtt_to_text(text, title)


tfj run addrtt1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py add_rtt/bot list"

https://github.com/wikimedia/popularpages

"""
# ---
import re
import tqdm
import wikitextparser as wtp

from newapi import printe
from newapi.mdwiki_page import NEW_API, md_MainPage, CatDepth
from pathlib import Path

Dir = Path(__file__).parent
# add_param_named(text, title)

api_new = NEW_API("www", family="mdwiki")
# api_new.Login_to_wiki()


def add_rtt_to_tables(text, pages):

    parsed = wtp.parse(text)

    for table in parsed.tables:
        for x in tqdm.tqdm(table.cells()):
            title = x[1].value.strip().replace("[[", "").replace("]]", "")
            r_s = x[2].value.strip()
            # ---
            # print(f"title: {title}, r_s: {r_s}")
            # ---
            if title in pages:
                x[2].value = "R"

    new_text = parsed.string
    return new_text


def work_page(pages):
    title = "WikiProjectMed:WikiProject Medicine/Popular pages"
    page = md_MainPage(title, "www", family="mdwiki")

    if not page.exists():
        return False

    text = page.get_text()

    newtext = add_rtt_to_tables(text, pages)

    if newtext != text:
        # ---
        with open(Dir / "test.txt", "w", encoding="utf-8") as f:
            f.write(newtext)
        # ---
        summary = "Added {{RTT}}"
        page.save(newtext=newtext, summary=summary, nocreate=1, minor="")


def main():

    # mdwiki_pages = CatDepth("Category:RTT", sitecode="www", family="mdwiki", depth=0, ns=0)
    temp_pages = api_new.Get_template_pages("Template:RTT", namespace=0)

    work_page(temp_pages)


if __name__ == "__main__":
    main()
