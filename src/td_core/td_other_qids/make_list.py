#!/usr/bin/python3
"""

Usage:
# python3 core8/pwb.py td_core/td_other_qids/make_list -td add
# python3 core8/pwb.py td_core/td_other_qids/make_list -others add
# python3 core8/pwb.py td_core/td_other_qids/make_list add

"""
import logging
import sys

from db.mdapi_sql.services import sql_qids, sql_qids_others
from md_core.p11143_bot.filter_helps import remove_in_db_elements
from md_core.unlinked_wb.bot import work_un
from td_core.td_other_qids.qids_help import (
    check_qids,
    get_o_qids_new,
    get_pages_to_work,
)

logger = logging.getLogger(__name__)


def add_q(new_qids, ty) -> None:
    # ---
    logger.info(f"len of new_qids: {len(new_qids)}")
    # ---
    if len(new_qids) == 0:
        return
    # ---
    if len(new_qids) < 10:
        logger.info("\n".join([f"{k}:{v}" for k, v in new_qids.items()]))
    # ---
    logger.info('<<puruple>> add "addq" to sys.argv to add them to qids')
    # ---
    if ty == "other":
        sql_qids_others.add_titles_to_qids(new_qids, add_empty_qid=True)
    else:
        sql_qids.add_titles_to_qids(new_qids, add_empty_qid=True)


def work_qids(ty, qids_list):
    # ---
    # qids_list = { x: y for x, y in qids_list.items() if y != ''}
    # ---
    work_list, all_pages = get_pages_to_work(ty)
    # ---
    o_qids = check_qids(work_list, all_pages, ty)
    o_qids = {x: v for x, v in o_qids.items() if x in work_list}
    # ---
    new_qids = get_o_qids_new(o_qids, qids_list)
    # ---
    logger.info(f"<<green>> new len of new_qids:{len(new_qids)}")
    # ---
    return new_qids


def start() -> None:
    # ---
    ALL_QIDS = {}
    # ---
    ALL_QIDS["other"] = sql_qids_others.get_others_qids()
    ALL_QIDS["td"] = sql_qids.get_all_qids()
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
        qids_list = ALL_QIDS[ty]
        new_qids = work_qids(ty, qids_list)
        work_un(new_qids)
        # ---
        new_qids = remove_in_db_elements(new_qids, ALL_QIDS["other"], ALL_QIDS["td"])
        # ---
        add_q(new_qids, ty)


if __name__ == "__main__":
    start()
