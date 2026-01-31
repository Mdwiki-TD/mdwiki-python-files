#!/usr/bin/python3
"""

from unlinked_wb.hlps import get_pages_in_use, get_qids

"""
# ---
import logging

from mdapi_sql import sql_for_mdwiki, sql_qids_others

logger = logging.getLogger(__name__)


def get_pages_in_use(all_pages):
    # ---
    pages_has = {}
    pages_hasnt = []
    # ---
    for x, ta in all_pages.items():
        qid = ta.get("pageprops", {}).get("unlinkedwikibase_id")
        if qid:
            pages_has[x] = qid
        else:
            pages_hasnt.append(x)
    # ---
    logger.info(f"<<yellow>> len of all_pages qids: {len(pages_has)}.")
    # ---
    # pages_props = api_new.pageswithprop(pwppropname="unlinkedwikibase_id", Max=500000)
    # pages = {x["title"]: x["value"] for x in pages_props}
    # logger.info(f"<<yellow>> len of : {len(pages)}.")
    # ---
    return pages_has, pages_hasnt


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
