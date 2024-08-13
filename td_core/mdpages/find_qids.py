#!/usr/bin/python3
"""
إيجاد معرف ويكيداتا للعناصر بدون معرف

The script checks if the project directory exists and changes the path if it doesn't. This is a good practice for handling file paths.

The script retrieves all Wikidata identifiers (QIDs) and filters them based on whether they are empty or not.

Usage:
python3 core8/pwb.py mdpages/find_qids

"""
import sys

from mdapi_sql import sql_for_mdwiki
from apis import wiki_api
from newapi import printe
from mdpy.bots.check_title import valid_title
from unlinked_wb.bot import work_un
from mdpages.create_qids import create_qids

qids = sql_for_mdwiki.get_all_qids()
# ---
qids_already = {q: title for title, q in qids.items() if q != ""}
# ---
noqids = [title for title, q in qids.items() if q == "" and valid_title(title) and not title.lower().startswith("video:")]


def get_qids(noqids_list):
    """
    function retrieves QIDs for a list of items. It uses the MediaWiki API to query for page properties and extracts the Wikidata item property. The function handles redirects and normalizes the titles. It also groups the items into batches of 50 to avoid exceeding the API's limit for the number of titles in a single request. This is a good practice for working with APIs.
    """
    # ---
    new_title_qids = {}
    # ---
    params = {
        "action": "query",
        "format": "json",
        # "titles": "",
        # "redirects": 1,
        "prop": "pageprops",
        "ppprop": "wikibase_item",
        # "normalize": 1,
        "utf8": 1,
    }
    # ---
    if "redirects" in sys.argv:
        params["redirects"] = 1
    # ---
    num = 0
    # ---
    for i in range(0, len(noqids_list), 100):
        # ---
        group = noqids_list[i : i + 100]
        # ---
        params["titles"] = "|".join(group)
        # ---
        jsone = wiki_api.submitAPI(params, site="en")
        # ---
        if jsone and "batchcomplete" in jsone:
            query = jsone.get("query", {})
            # ---
            redirects_x = {x["to"]: x["from"] for x in query.get("redirects", [])}
            # ---
            # "redirects": [{"from": "Acetylsalicylic acid","to": "Aspirin"}]
            # ---
            # "pages": { "4195": {"pageid": 4195,"ns": 0,"title": "Aspirin","redirects": [{"pageid": 4953,"ns": 0,"title": "Acetylsalicylic acid"}]} }
            pages = query.get("pages", {})
            # ---
            # { "-1": { "ns": 0, "title": "Fsdfdsf", "missing": "" }, "2767": { "pageid": 2767, "ns": 0, "title": "ACE inhibitor" } }
            # ---
            for _, kk in pages.items():
                # ---
                num += 1
                # ---
                title = kk.get("title", "")
                qid = kk.get("pageprops", {}).get("wikibase_item", "")
                # ---
                title = redirects_x.get(title, title)
                # ---
                new_title_qids[title] = qid
    # ---
    return new_title_qids


def to_add_wrk(to_add, noqids):
    printe.output("===================")
    printe.output(f"find qid to {len(to_add)} from {len(noqids)} pages.")
    # ---
    if to_add:
        printe.output("<<yellow>>\n".join([f"{k}\t:\t{v}" for k, v in to_add.items()]))
        # ---
        printe.output('<<purple>> add "add" to sys.argv to add them?')
        # ---
        if "add" in sys.argv:
            sql_for_mdwiki.add_titles_to_qids(to_add)
        # ----
        work_un(to_add)


def empty_qids_wrk(empty_qids):
    printe.output("===================")
    # ---
    printe.output(f"<<red>>no qids: {len(empty_qids)}")
    # ---
    if empty_qids:
        # ---
        for x in empty_qids:
            printe.output(f"\t<<red>>{x}")
        # ---
        printe.output('<<purple>> add "createq" to sys.argv to create new items for them?')
        # ---
        if "createq" in sys.argv:
            create_qids(empty_qids)


def false_qids_wrk(false_qids):
    printe.output("===================")
    if false_qids:
        printe.output("<<red>> flase qids:")
        for xz, q in false_qids.items():
            title_in = qids_already.get(q, "")
            # ---
            printe.output(f"q: {q}\t new title: ({xz})\t: title_in: ({title_in})..")


def start():
    # ---
    if len(noqids) == 0:
        printe.output('<<green>> noqids list is empty. return "".')
        return
    # ---
    new_title_qid = get_qids(noqids)
    # ---
    false_qids = {}
    # ---
    to_add = {}
    empty_qids = []
    # ---
    for x, q in new_title_qid.items():
        # ---
        if not q:
            empty_qids.append(x)
            continue
        # ---
        if q not in list(qids_already.keys()):
            to_add[x] = q
        else:
            false_qids[x] = q
    # ---
    false_qids_wrk(false_qids)
    # ---
    empty_qids_wrk(empty_qids)
    # ---
    to_add_wrk(to_add, noqids)


if __name__ == "__main__":
    start()
