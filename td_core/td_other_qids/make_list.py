#!/usr/bin/python3
"""

Usage:
# python3 core8/pwb.py td_other_qids/make_list -td add
# python3 core8/pwb.py td_other_qids/make_list -others add
# python3 core8/pwb.py td_other_qids/make_list add

"""
import sys

from mdapi_sql import sql_for_mdwiki, sql_qids_others
from mdpages import qids_help
from newapi import printe
from p11143_bot.filter_helps import remove_in_db_elements
from unlinked_wb.bot import work_un

ALL_QIDS = {}


def add_q(new_qids, ty):
    # ---
    printe.output(f"len of new_qids: {len(new_qids)}")
    # ---
    if len(new_qids) == 0:
        return
    # ---
    new_qids = remove_in_db_elements(new_qids, ALL_QIDS["other"], ALL_QIDS["td"])
    # ---
    if len(new_qids) < 10:
        printe.output("\n".join([f"{k}:{v}" for k, v in new_qids.items()]))
    # ---
    printe.output('<<puruple>> add "addq" to sys.argv to add them to qids')
    # ---
    if ty == "other":
        sql_qids_others.add_titles_to_qids(new_qids, add_empty_qid=True)
    else:
        sql_for_mdwiki.add_titles_to_qids(new_qids, add_empty_qid=True)


def work_qids(ty):
    # ---
    qids_list = ALL_QIDS[ty]
    # ---
    # qids_list = { x: y for x, y in qids_list.items() if y != ''}
    # ---
    work_list, all_pages = qids_help.get_pages_to_work(ty)
    # ---
    o_qids = qids_help.check(work_list, all_pages, ty)
    o_qids = {x: v for x, v in o_qids.items() if x in work_list}
    # ---
    new_qids = qids_help.get_o_qids_new(o_qids, qids_list)
    # ---
    printe.output(f"<<green>> new len of new_qids:{len(new_qids)}")
    # ---
    work_un(new_qids)
    # ---
    add_q(new_qids, ty)


def start():
    # ---
    ALL_QIDS["other"] = sql_qids_others.get_others_qids()
    ALL_QIDS["td"] = sql_for_mdwiki.get_all_qids()
    # ---
    tab = ["td"]
    # ---
    if "-others" in sys.argv:
        tab = ["other"]
    # ---
    if "all" in sys.argv:
        tab = ["td", "other"]
    # ---
    for ty in tab:
        work_qids(ty)


if __name__ == "__main__":
    start()
