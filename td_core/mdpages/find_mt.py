"""

Usage:
python3 core8/pwb.py mdpages/find_mt

ايحاد العناوين المكررة بين قاعدتي البيانات
sql_for_mdwiki
sql_qids_others

"""

import logging
import sys

from apis import cat_cach
from mdapi_sql import sql_for_mdwiki, sql_qids_others
from mdpy.bots.check_title import valid_title

logger = logging.getLogger(__name__)


def remove_from_others(qids_othrs, qids_td):
    # ---
    TD_list = cat_cach.from_cache()
    # ---
    in_both = [x for x in qids_othrs if x in qids_td]
    # ---
    in_both.extend([x for x in qids_td if x in qids_othrs])
    # ---
    in_both = list(set(in_both))
    # ---
    same_q = [x for x in in_both if qids_othrs[x] == qids_td[x]]
    diff_q = [x for x in in_both if qids_othrs[x] != qids_td[x]]
    # ---
    printe.output(f"<<yellow>> len of in_both list: {len(in_both):,}, same_q: {len(same_q):,}, diff_q: {len(diff_q):,}")
    # ---
    for n, title in enumerate(diff_q, start=1):
        qid_td = qids_td[title]
        qid_othrs = qids_othrs[title]
        # ---
        printe.output(f"t: {n}/{len(diff_q)}\t {title=} \t {qid_othrs} \t {qid_td=}")
        # ---
        # sql_qids_others.set_title_where_qid(title, qid_othrs)
    # ---
    same_q_in_td = [x for x in same_q if x in TD_list]
    # ---
    printe.output(
        f"<<yellow>> len of list: {len(same_q_in_td)=:,}, add 'delete' to sys.argv to delete them from sql_qids_others."
    )
    # ---
    if "delete" in sys.argv:
        for n, title in enumerate(same_q_in_td, start=1):
            sql_qids_others.delete_title_from_db(title, pr=f"{n}/{len(same_q_in_td)}")


def doo():
    # ---
    qids_othrs = sql_qids_others.get_others_qids()
    print(f"len of qids_othrs: {len(qids_othrs):,}")

    # ---
    qids_td = sql_for_mdwiki.get_all_qids()
    print(f"len of qids_td: {len(qids_td):,}")

    # ---
    to_work = [title for title, q in qids_td.items() if q == "" and valid_title(title)]
    printe.output(f"<<green>> len of to_work list: {len(to_work)}")

    # ---
    new_qids = {x: qids_othrs[x] for x in to_work if x in qids_othrs}
    printe.output(f"<<green>> new_qids list: {len(new_qids)}")

    # ---
    if to_work and new_qids:
        sql_for_mdwiki.add_titles_to_qids(new_qids)

    # ---
    remove_from_others(qids_othrs, qids_td)


if __name__ == "__main__":
    doo()
