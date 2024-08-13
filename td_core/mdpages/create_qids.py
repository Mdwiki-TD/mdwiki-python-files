#!/usr/bin/python3
"""
Usage:

python3 core8/pwb.py mdpages/create_qids

from mdpages.create_qids import create_qids

"""
from mdapi_sql import sql_for_mdwiki
from apis import wikidataapi
from unlinked_wb.bot import add_un_linked_wb


def create_qids(no_qids):
    """
    create wikidata item for qids
    creates new Wikidata items for those without QIDs. It uses a for loop to iterate over the list of items without QIDs and makes a POST request to the Wikidata API for each item. The function also prints the response from the API, which can be useful for debugging.
    """
    # ---
    for x in no_qids:
        # ---
        new_qid = wikidataapi.new_item(label="", lang="", returnid=True)
        # ---
        if not new_qid or not str(new_qid).startswith("Q"):
            print(f"Skip.. {new_qid=}")
            continue
        # ---
        wikidataapi.Claim_API_str(new_qid, "P11143", x)
        # ---
        # add new qid to article
        add_un_linked_wb(x, new_qid)
        # ---
        # add new qid to db
        sql_for_mdwiki.add_titles_to_qids({x: new_qid})
