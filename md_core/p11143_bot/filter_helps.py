"""
Usage:
from p11143_bot.filter_helps import remove_in_db_elements

"""

import logging

logger = logging.getLogger(__name__)


def remove_in_db_elements(qids_x, list_1, list_2):
    # ---
    n_qids = {}
    # ---
    for qid, title in qids_x.items():
        if list_1.get(title) == qid:
            continue
        # ---
        if list_2.get(title) == qid:
            continue
        # ---
        n_qids[qid] = title
    # ---
    logger.info(f"remove_in_db_elements new len: {len(n_qids):,}")
    # ---
    return n_qids
