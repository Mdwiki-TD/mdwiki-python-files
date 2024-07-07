#!/usr/bin/python3
"""
This script performs various operations related to MediaWiki pages and Wikibase QIDs.
It includes functions for filtering and processing page titles, checking page existence,
retrieving and modifying page content, and adding tags based on QIDs.

Usage:
python3 core8/pwb.py unlinked_wb/bot add
"""
# ---
import re
import sys
from mdpy.bots import sql_for_mdwiki
from mdpy.bots.check_title import valid_title
from newapi import printe
from mdpy.bots import sql_qids_others

# ---
from newapi.mdwiki_page import NEW_API, MainPage as md_MainPage

api_new = NEW_API("www", family="mdwiki")
api_new.Login_to_wiki()


def get_qids():
    qids1 = sql_for_mdwiki.get_all_qids()
    qids2 = sql_qids_others.get_others_qids()
    # ---
    qids1 = {x: v for x, v in qids1.items() if v != ""}
    qids2 = {x: v for x, v in qids2.items() if v != ""}
    # ---
    vals_d = {}
    # ---
    for tab in [qids1, qids2]:
        for x, q in tab.items():
            if q not in vals_d:
                vals_d[q] = [x]
            elif x not in vals_d[q]:
                vals_d[q].append(x)
    # ---
    qids = {v[0]: q for q, v in vals_d.items() if len(v) == 1}
    # ---
    return qids, vals_d


def work_un_linked_wb(title, qid):
    # ---
    page = md_MainPage(title, "www", family="mdwiki")
    # ---
    exists = page.exists()
    if not exists:
        return
    # ---
    # if page.isRedirect() :  return
    # target = page.get_redirect_target()
    # ---
    text = page.get_text()
    # refs        = page.Get_tags(tag='ref')# for x in ref: name, contents = x.name, x.contents
    # templates = page.get_templates()
    # ---
    # get qid
    patern = r"\{\{#unlinkedwikibase:id=(Q\d+)\}\}"
    # ---
    if text.find("{{#unlinkedwikibase:id=") != -1:
        # ---
        qid_in = ""
        # ---
        m = re.search(patern, text)
        if m:
            printe.output("no qid in text")
            qid_in = m.group(1)
        # ---
        printe.output(f"page already tagged. {qid_in=}, {qid=}")
        return
    # ---
    tag = "{{#unlinkedwikibase:id=" + qid + "}}\n"
    # ---
    newtext = tag + text.strip()
    # ---
    page.save(newtext=newtext, summary="add tag:" + tag, nocreate=1, minor="")


def work_un(tab):
    for numb, (title, new_q) in enumerate(tab.items(), start=1):
        # ---
        printe.output(f"<<yellow>> work_un: {numb}, {title=}, {new_q=}")
        # ---
        if new_q:
            work_un_linked_wb(title, new_q)


def get_pages_in_use():
    pages_props = api_new.pageswithprop(pwppropname="unlinkedwikibase_id", Max=50000)
    # ---
    pages = {x["title"]: x["value"] for x in pages_props}
    # ---
    printe.output(f"<<yellow>> len of get_pages_in_use: {len(pages)}.")
    # ---
    return pages


def add_to_pages(pages_to_add):
    # ---
    for n, (x, qid) in enumerate(pages_to_add.items(), start=1):
        printe.output(f"p:{n}/{len(pages_to_add)}: t:{x}::")
        # ---
        if not qid:
            printe.output("no qid")
            continue
        # ---
        work_un_linked_wb(x, qid)


def pages_has_to_work(qids, pages_has):
    # ---
    f_to_work = {page: qids[page] for page in pages_has if page in qids}
    # ---
    printe.output(f"len of pages_has: {len(pages_has)}, f_to_work: {len(f_to_work)}")
    # ---
    for n, (x, qid) in enumerate(f_to_work.items(), start=1):
        printe.output(f"p:{n}/{len(f_to_work)}: t:{x}::")
        # ---
        if not qid:
            printe.output("no qid")
            continue
        # ---
        work_un_linked_wb(x, qid)


def add_tag():
    # ---
    printe.output("Get all pages...")
    # ---
    qids, vals_d = get_qids()
    # ---
    all_pages = api_new.Get_All_pages(start="!", namespace="0", apfilterredir="nonredirects")
    # ---
    all_pages = [x for x in all_pages if valid_title(x)]
    # ---
    pages_has = get_pages_in_use()
    # ---
    pages_to_add = {page: qids[page] for page in all_pages if page in qids and page not in pages_has}
    # ---
    printe.output(f"len of all_pages: {len(all_pages)}, pages_to_add: {len(pages_to_add)}")
    # ---
    add_to_pages(pages_to_add)
    # ---
    pages_has_to_work(qids, pages_has)
    # ---
    for q, v in vals_d.items():
        if len(v) > 1:
            printe.output(f"<<red>> duplicate: q:{q}, v:{v}")


if __name__ == "__main__":
    add_tag()
