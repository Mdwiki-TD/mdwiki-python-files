#!/usr/bin/python3
"""
python3 core8/pwb.py mdpy/sql_qids_others

# ---
from mdpages.qids_others import sql_qids_others
# sql_qids_others. select_md_sql(query, return_dict=False, values=None)
# sql_qids_others. mdwiki_sql(query, return_dict=False, values=None)
# sql_qids_others. get_others_qids()
# sql_qids_others. set_title_where_qid(new_title, qid)
# sql_qids_others. add_titles_to_qids(tab, add_empty_qid=False)
# ---
"""
import logging

from mdapi_sql import sql_td_bot

logger = logging.getLogger(__name__)

# result = sql_td_bot.sql_connect_pymysql(query, return_dict=return_dict, values=values)


def mdwiki_sql(query, return_dict=False, values=None, **kwargs):
    # ---
    if not query:
        logger.info("query == ''")
        return {}
    # ---
    # logger.info('<<yellow>> newsql::')
    return sql_td_bot.sql_connect_pymysql(query, return_dict=return_dict, values=values)


def select_md_sql(query, *args, **kwargs):
    # ---
    if not query:
        logger.info("query == ''")
        return {}
    # ---
    return mdwiki_sql(query, *args, **kwargs)


def get_others_qids():
    # ---
    # xxxx iiii oooo gggg
    # ---
    sq = select_md_sql("select DISTINCT title, qid from qids_others;", return_dict=True)
    return {ta["title"]: ta["qid"] for ta in sq}


def add_qid(title, qid):
    logger.info(f"<<yellow>> () title:{title}, qid:{qid}")
    # ---
    qua_old = "INSERT INTO qids_others (title, qid) SELECT %s, %s;"
    # ---
    qua = """
        INSERT INTO qids_others (title, qid)
        SELECT %s, %s
        WHERE NOT EXISTS ( SELECT 1 FROM qids WHERE title = %s and qid = %s)
        AND NOT EXISTS   (SELECT 1 FROM qids_others WHERE title = %s and qid = %s)
        ;
        """
    # ---
    values = [title, qid, title, qid, title, qid]
    # ---
    return mdwiki_sql(qua, return_dict=True, values=values)


def set_qid_where_qid(new_qid, old_qid):
    logger.info(f"<<yellow>> () new_qid:{new_qid}, old_qid:{old_qid}")
    # ---
    qua = "UPDATE qids_others set qid = %s where qid = %s;"
    values = [new_qid, old_qid]
    # ---
    return mdwiki_sql(qua, return_dict=True, values=values)


def set_qid_where_title(title, qid):
    logger.info(f"<<yellow>> () title:{title}, qid:{qid}")
    # ---
    qua = "UPDATE qids_others set qid = %s where title = %s;"
    values = [qid, title]
    # ---
    return mdwiki_sql(qua, return_dict=True, values=values)


def delete_title_from_db(title, pr=""):
    qua = "DELETE FROM qids_others where title = %s;"
    # ---
    logger.info(f"<<yellow>> {pr} (qids_others) title:{title}")
    # ---
    return mdwiki_sql(qua, return_dict=True, values=[title])


def set_title_where_qid(new_title, qid):
    # ---
    logger.info(f"<<yellow>> () new_title:{new_title}, qid:{qid}")
    # ---
    qua = "UPDATE qids_others set title = %s where qid = %s;"
    values = [new_title, qid]
    # ---
    return mdwiki_sql(qua, return_dict=True, values=values)


def qids_set_title_where_title_qid(old_title, new_title, qid, no_do=False):
    # ---
    qua = "UPDATE qids_others set title = %s where qid = %s and title = %s;"
    values = [new_title, qid, old_title]
    # ---
    if no_do:
        logger.info(qua % (f'"{new_title}"', f'"{qid}"', f'"{old_title}"'))
        return
    # ---
    logger.info(f"<<yellow>> () {new_title=}, {qid=}, {old_title=}")
    # ---
    return mdwiki_sql(qua, return_dict=True, values=values)


def add_titles_to_qids(tab0, add_empty_qid=False):
    # ---
    logger.info(f"<<green>> start {add_empty_qid=}:")
    # ---
    if not tab0:
        logger.info("<<red>> tab0 empty..")
        return
    # ---
    ids_in_db = get_others_qids()
    # ---
    # remove empty titles
    # remove empty qids if add_empty_qid == False
    tab = {t: q for t, q in tab0.items() if t.strip() and (q.strip() or add_empty_qid)}
    # ---
    logger.info(f"<<yellow>> len of tab: {len(tab)}, tab0: {len(tab0)}")
    # ---
    same = {x: qid for x, qid in tab.items() if qid == ids_in_db.get(x)}
    not_in = {x: qid for x, qid in tab.items() if x not in ids_in_db}
    # ---
    logger.info(f"<<yellow>> len of ids_in_db: {len(ids_in_db)}")
    logger.info(f"<<yellow>> len of same qids: {len(same)}")
    logger.info(f"<<yellow>> len of not_in: {len(not_in)}")
    # ---
    for title, new_qid in not_in.items():
        add_qid(title, new_qid)
    # ---
    rest_qids = {x: qid for x, qid in tab.items() if x not in same and x not in not_in}
    # ---
    logger.info(f"<<yellow>> len of rest_qids: {len(rest_qids)}.")
    # ---
    rest_qids = {x: qid for x, qid in rest_qids.items() if qid}
    # ---
    logger.info(f"<<yellow>> len of rest_qids: {len(rest_qids)} after remove empty qids..")
    # ---
    if not rest_qids:
        return
    # ---
    for title, new_qid in rest_qids.items():
        # ---
        if not ids_in_db.get(title):
            set_qid_where_title(title, new_qid)
    # ---
    has_diff_qid_in_db = {x: qid for x, qid in rest_qids.items() if ids_in_db.get(x)}
    # ---
    logger.info(f"<<yellow>> len of last_qids: {len(has_diff_qid_in_db)} after remove titles in db..")
    # ---
    for t, q in has_diff_qid_in_db.items():
        qid_in = ids_in_db.get(t)
        logger.info(f"<<yellow>>skip... set_qid_where_title({t=}) {qid_in=}, {q=}")


if __name__ == "__main__":
    # python3 core8/pwb.py md_core_helps/mdapi_sql/sql_for_mdwiki
    d = get_others_qids()
    logger.info(f"{len(d)=}")
