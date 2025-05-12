#!/usr/bin/python3
"""

python3 core8/pwb.py add_rtt/pup
from add_rtt.bot import add_rtt_to_text
# add_rtt_to_text(text, title)


tfj run addrtt1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py add_rtt/pup"

https://github.com/wikimedia/popularpages

"""
# ---
import re
import tqdm
import wikitextparser as wtp

from newapi import printe
from newapi.mdwiki_page import NEW_API, md_MainPage  # , CatDepth
from pathlib import Path

Dir = Path(__file__).parent
# add_param_named(text, title)

api_new = NEW_API("www", family="mdwiki")
# api_new.Login_to_wiki()


def fix_title(title):
    title = title.replace("[[", "").replace("]]", "")
    title = title.replace("&#039;", "'")
    # ---
    return title


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
    printe.output(f"find_redirects pages: {len(mdwiki_pages)}")
    # ---
    titles = api_new.get_titles_redirects(mdwiki_pages)
    # ---
    # titles = api_new.get_titles_redirects(["Ehlers–Danlos syndrome"]) # {'Ehlers–Danlos syndrome': 'Ehlers–Danlos syndromes'}
    redirects = {x: y for x, y in titles.items()}
    # ---
    return redirects


def add_rtt_to_tables(text, pages):
    # ---
    parsed = wtp.parse(text)
    # ---
    already_in = []
    no_add = []
    # ---
    add_from_redirect = []
    add_done = []
    # ---
    redirects = find_redirects(pages, text)
    # ---
    def mark_as_reviewed(cell):
        cell.value = "R"
        cell.set_attr("style", "text-align:center; white-space:nowrap; font-weight:bold; background:#C66A05")  # ffd6ff
    # ---
    for table in parsed.tables:
        # ---
        for x in tqdm.tqdm(table.cells()):
            # ---
            title = x[2].value.strip()
            r_s = x[1].value.strip()
            # ---
            if x[1].is_header:
                continue
            # ---
            title = fix_title(title)
            # ---
            title2 = redirects.get(title, title)
            # ---
            if r_s == "R":
                mark_as_reviewed(x[1])
                # ---
                already_in.append(title)
                continue
            # ---
            # print(f"title: ({title}), r_s: ({r_s})")
            # ---
            if title in pages:
                mark_as_reviewed(x[1])
                # ---
                add_done.append(title)
            elif title2 in pages:
                mark_as_reviewed(x[1])
                # ---
                add_from_redirect.append(title)
            else:
                no_add.append(title)
    # ---
    printe.output(f"<<yellow>> no_add: {len(no_add)}, already_in: {len(already_in)}")
    # ---
    printe.output(f"<<yellow>> add_done: {len(add_done)}, add_from_redirect: {len(add_from_redirect)}")
    # ---
    new_text = parsed.string
    # ---
    return new_text


def work_page(pages):
    title = "WikiProjectMed:WikiProject Medicine/Popular pages"
    page = md_MainPage(title, "www", family="mdwiki")

    if not page.exists():
        return False

    text = page.get_text()

    newtext = add_rtt_to_tables(text, pages)

    with open(Dir / "test.txt", "w", encoding="utf-8") as f:
        f.write(newtext)

    if newtext == text:
        printe.output("no changes")
        return False

    summary = "Added {{RTT}}"

    page.save(newtext=newtext, summary=summary, nocreate=1, minor="")


def main():

    # mdwiki_pages = CatDepth("Category:RTT", sitecode="www", family="mdwiki", depth=0, ns=0)
    temp_pages = api_new.Get_template_pages("Template:RTT", namespace=0)

    work_page(temp_pages)


if __name__ == "__main__":
    main()
