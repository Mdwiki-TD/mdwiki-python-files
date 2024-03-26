#!/usr/bin/python3
"""

Usage:
# python3 core8/pwb.py td_other_qids/make_list td add
# python3 core8/pwb.py td_other_qids/make_list other add
# python3 core8/pwb.py td_other_qids/make_list add

"""
import sys

# ---
from mdpy.bots import sql_qids_others
from mdpy.bots import sql_for_mdwiki
from unlinked_wb.bot import work_un
# ---
from mdpages import qids_help
# qids_help.get_o_qids_new(o_qids, t_qids_in)
# qids_help.get_pages_to_work(ty="td|other")
# qids_help.check(work_list, all_pages)
# ---
medwiki_to_enwiki_conflic = {}
medwiki_to_enwiki = {}
# ---
# mdtitle_to_qid = sql_qids_others.get_others_qids()
# sql_qids_others.add_titles_to_qids(tab, add_empty_qid=False)
# sql_qids_others.set_title_where_qid(new_title, qid)
# ---
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# sql_for_mdwiki.add_titles_to_qids(tab, add_empty_qid=False)
# sql_for_mdwiki.set_title_where_qid(new_title, qid)

def wrk_in(ty, t_qids_in):
    # ---
    work_list, all_pages = qids_help.get_pages_to_work(ty)
    # ---
    o_qids = qids_help.check(work_list, all_pages)
    o_qids = {x: v for x, v in o_qids.items() if x in work_list}
    # ---
    # write to sql
    o_qids_new = qids_help.get_o_qids_new(o_qids, t_qids_in)
    # ---
    return o_qids_new


def start():
    # ---
    ty = "other" if "other" in sys.argv else "td"
    # ---
    if ty == "other":
        t_qids_in = sql_qids_others.get_others_qids()
    else:
        t_qids_in = sql_for_mdwiki.get_all_qids()
    # ---
    # t_qids_in = { x: y for x, y in t_qids_in.items() if y != ''}
    # ---
    o_qids_new = wrk_in(ty, t_qids_in)
    # ---
    if "add" in sys.argv:
        if ty == "other":
            sql_qids_others.add_titles_to_qids(o_qids_new, add_empty_qid=True)
        else:
            sql_for_mdwiki.add_titles_to_qids(o_qids_new, add_empty_qid=True)
    # ---
    work_un(o_qids_new)

if __name__ == "__main__":
    start()
