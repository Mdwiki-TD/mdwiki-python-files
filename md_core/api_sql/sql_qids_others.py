#!/usr/bin/python3
"""
# ---
from mdpages.qids_others import sql_qids_others
# mdtitle_to_qid = sql_qids_others.get_others_qids()
# sql_qids_others.add_titles_to_qids(tab, add_empty_qid=False)
# sql_qids_others.set_title_where_qid(new_title, qid)
# ---
"""
#
#
#
from newapi import printe
from api_sql import sql_for_mdwiki

# sql_for_mdwiki.mdwiki_sql(query, update = False)
# ---


def get_others_qids():
    # ---
    mdtitle_to_qid = {}
    # ---
    sq = sql_for_mdwiki.mdwiki_sql("select DISTINCT title, qid from qids_others;", return_dict=True)
    # ---
    for ta in sq:
        mdtitle_to_qid[ta["title"]] = ta["qid"]
    # ---
    return mdtitle_to_qid


def add_qid(title, qid):
    qua = "INSERT INTO qids_others (title, qid) SELECT %s, %s;"
    # ---
    printe.output(f"<<yellow>> add_qid()  title:{title}, qid:{qid}")
    # ---
    return sql_for_mdwiki.mdwiki_sql(qua, return_dict=True, values=[title, qid])


def set_qid_where_title(title, qid):
    qua = "UPDATE qids_others set qid = %s where title = %s;"
    # ---
    printe.output(f"<<yellow>> set_qid_where_title()  title:{title}, qid:{qid}")
    # ---
    return sql_for_mdwiki.mdwiki_sql(qua, return_dict=True, values=[qid, title])


def set_title_where_qid(new_title, qid):
    qua = "UPDATE qids_others set title = %s where qid = %s;"
    # ---
    printe.output(f"<<yellow>> set_title_where_qid() new_title:{new_title}, qid:{qid}")
    # ---
    return sql_for_mdwiki.mdwiki_sql(qua, return_dict=True, values=[new_title, qid])


def add_titles_to_qids(tab, add_empty_qid=False):
    # ---
    new = {}
    # ---
    if not tab:
        printe.output("<<red>> add_titles_to_qids tab empty..")
        return
    # ---
    for title, qid in tab.items():
        # ---
        if not title:
            print("title == ''")
            continue
        # ---
        if qid == "" and not add_empty_qid:
            print("qid == ''")
            continue
        # ---
        new[title] = qid
    # ---
    others_in = get_others_qids()
    # ---
    same = 0
    # ---
    for title, qid in new.items():
        if title not in others_in:
            add_qid(title, qid)
            continue
        # ---
        q_in = others_in[title]
        # ---
        if qid != "":
            if not q_in:
                set_qid_where_title(title, qid)
            else:
                if qid != q_in:
                    printe.output(f"<<yellow>> set_qid_where_title() qid_in:{q_in}, new_qid:{qid}")
                else:
                    same += 1
        # ---
    # ---
    printe.output(f"<<yellow>> len of same qids: {same}")
