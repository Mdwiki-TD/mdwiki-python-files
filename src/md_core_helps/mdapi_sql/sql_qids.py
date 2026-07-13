#!/usr/bin/python3
"""
python3 core8/pwb.py md_core/mdpy/sql_qids
"""
import logging

from md_core_helps.mdapi_sql.sql_td_bot import toolforge_tools_sql_connect

logger = logging.getLogger(__name__)


def _mdwiki_sql(query, values=None):
    # ---
    if not query:
        logger.info("query == ''")
        return {}
    # ---
    return toolforge_tools_sql_connect(
        query,
        return_dict=True,
        values=values,
        many=False,
    )


def get_all_qids():
    # ---
    # xxxx iiii oooo gggg
    # ---
    sq = _mdwiki_sql("select DISTINCT title, qid from qids;")
    return {ta["title"]: ta["qid"] for ta in sq}


def add_qid(title, qid):
    logger.info(f"<<yellow>> () title:{title}, qid:{qid}")
    qua = """
        INSERT INTO qids (title, qid)
        SELECT %s, %s
        WHERE NOT EXISTS ( SELECT 1 FROM qids WHERE title = %s and qid = %s)
        AND NOT EXISTS   (SELECT 1 FROM qids_others WHERE title = %s and qid = %s)
        ;
        """
    # ---
    values = [title, qid, title, qid, title, qid]
    # ---
    return _mdwiki_sql(qua, values=values)


def set_qid_where_qid(new_qid, old_qid):
    logger.info(f"<<yellow>> () new_qid:{new_qid}, old_qid:{old_qid}")
    # ---
    qua = "UPDATE qids set qid = %s where qid = %s;"
    values = [new_qid, old_qid]
    # ---
    return _mdwiki_sql(qua, values=values)


def set_qid_where_title(title, qid):
    logger.info(f"<<yellow>> () title:{title}, qid:{qid}")
    # ---
    qua = "UPDATE qids set qid = %s where title = %s;"
    values = [qid, title]
    # ---
    return _mdwiki_sql(qua, values=values)


def delete_title_from_db(title, pr: str = ""):
    qua = "DELETE FROM qids where title = %s;"
    # ---
    logger.info(f"<<yellow>> {pr} (qids) title:{title}")
    # ---
    return _mdwiki_sql(qua, values=[title])


def set_title_where_qid(new_title, qid):
    # ---
    logger.info(f"<<yellow>> () new_title:{new_title}, qid:{qid}")
    # ---
    qua = "UPDATE qids set title = %s where qid = %s;"
    values = [new_title, qid]
    # ---
    return _mdwiki_sql(qua, values=values)


def qids_set_title_where_title_qid(old_title, new_title, qid, no_do: bool = False):
    # ---
    qua = "UPDATE qids set title = %s where qid = %s and title = %s;"
    values = [new_title, qid, old_title]
    # ---
    if no_do:
        logger.info(qua % (f'"{new_title}"', f'"{qid}"', f'"{old_title}"'))
        return None
    # ---
    logger.info(f"<<yellow>> () {new_title=}, {qid=}, {old_title=}")
    # ---
    return _mdwiki_sql(qua, values=values)


def add_titles_to_qids(tab0, add_empty_qid: bool = False) -> None:
    # ---
    logger.info(f"<<green>> start {add_empty_qid=}:")
    # ---
    if not tab0:
        logger.info("<<red>> tab0 empty..")
        return
    # ---
    ids_in_db = get_all_qids()
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
    d = add_qid("Zolpidem", "Q218842")
    logger.info(f"{len(d)=}")
