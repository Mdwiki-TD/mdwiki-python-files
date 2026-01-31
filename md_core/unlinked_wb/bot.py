#!/usr/bin/python3
"""
This script performs various operations related to MediaWiki pages and Wikibase QIDs.
It includes functions for filtering and processing page titles, checking page existence,
retrieving and modifying page content, and adding tags based on QIDs.

Usage:
    python3 core8/pwb.py unlinked_wb/bot

"""
from unlinked_wb.hlps import get_pages_in_use, get_qids
from newapi.mdwiki_page import NEW_API, md_MainPage
import logging

# ---
import re
import sys

from mdpy.bots.check_title import valid_title

logger = logging.getLogger(__name__)

api_new = NEW_API("www", family="mdwiki")
# api_new.Login_to_wiki()


def add_un_linked_wb(title, qid):
    # ---
    page = md_MainPage(title, "www", family="mdwiki")
    # ---
    if not page.exists():
        return False
    # ---
    # if page.isRedirect() :  return
    # target = page.get_redirect_target()
    # ---
    text = page.get_text()
    # refs        = page.Get_tags(tag='ref')# for x in ref: name, contents = x.name, x.contents
    # templates = page.get_templates()
    # ---
    # get qid
    pattern = r"\{\{#unlinkedwikibase:id=(Q\d+)\}\}"
    # ---
    if text.find("{{#unlinkedwikibase:id=") != -1:
        # ---
        qid_in = ""
        # ---
        m = re.search(pattern, text)
        if m:
            qid_in = m.group(1)
        # ---
        printe.output(f"page already tagged.{title=}\t{qid_in=}\t{qid=}")
        return False
    # ---
    tag = "{{#unlinkedwikibase:id=" + qid + "}}\n"
    # ---
    newtext = tag + text.strip()
    # ---
    save = page.save(newtext=newtext, summary="add tag:" + tag, nocreate=1, minor="")
    # ---
    return save


def work_un(tab):
    for numb, (title, new_q) in enumerate(tab.items(), start=1):
        # ---
        printe.output(f"-----------------\n<<yellow>> work_un: {numb}, {title=}, {new_q=}")
        # ---
        if new_q:
            add_un_linked_wb(title, new_q)


def add_to_pages(pages_to_add):
    # ---
    if "noadd" in sys.argv:
        return
    # ---
    for n, (x, qid) in enumerate(pages_to_add.items(), start=1):
        printe.output(f"-----------------\np:<<yellow>> {n}/{len(pages_to_add)}: t:{x}::")
        # ---
        if not qid:
            printe.output("no qid")
            continue
        # ---
        add_un_linked_wb(x, qid)


def pages_has_to_work(qids, pages_has):
    # ---
    f_to_work = {page: qids[page] for page in pages_has if page in qids and qids[page] != pages_has[page]}
    # ---
    printe.output(f"len of pages_has: {len(pages_has)}, f_to_work: {len(f_to_work)}")
    # ---
    for n, (x, qid) in enumerate(f_to_work.items(), start=1):
        printe.output("<<yellow>>-----------------")
        # ---
        printe.output(f"p:{n}/{len(f_to_work)}: t:{x}::")
        # ---
        if not qid:
            printe.output("no qid")
            continue
        # ---
        add_un_linked_wb(x, qid)


def add_tag():
    # ---
    printe.output("Get all pages...")
    # ---
    qids, vals_d = get_qids()
    # ---
    # all_pages = api_new.Get_All_pages(start="", namespace="0", apfilterredir="nonredirects", ppprop="")
    all_pages_tab = api_new.Get_All_pages_generator(
        start="",
        namespace="0",
        limit="max",
        filterredir="nonredirects",
        ppprop="unlinkedwikibase_id",
        limit_all=100000,
    )
    # ---
    pages_has, pages_hasnt = get_pages_in_use(all_pages_tab)
    # ---
    all_pages = [x for x in all_pages_tab if valid_title(x)]
    # ---
    printe.output(f"<<purple>> {len(all_pages)=}, {len(pages_has)=}")
    # ---
    pages_to_add = {page: qids[page] for page in pages_hasnt if page in qids}
    # ---
    printe.output(f"<<purple>> {len(pages_hasnt)=}, {len(pages_to_add)=}")
    # ---
    pages_has_to_work(qids, pages_has)
    # ---
    add_to_pages(pages_to_add)
    # ---
    for q, v in vals_d.items():
        if len(v) > 1:
            printe.output(f"<<red>> duplicate: q:{q}, v:{v}")


if __name__ == "__main__":
    add_tag()
