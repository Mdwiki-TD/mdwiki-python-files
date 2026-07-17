"""
python3 core8/pwb.py td_core/td_other_qids/fix_qids all
python3 core8/pwb.py td_core/td_other_qids/fix_qids -others
python3 core8/pwb.py td_core/td_other_qids/fix_qids td
python3 core8/pwb.py td_core/td_other_qids/fix_qids redirects

"""

import logging
import sys

from db.tools.services.wikidata.qid_service import (
    get_title_to_qid,
    update_qid_by_value,
    batch_upsert_qids,
)
from db.tools.services.wikidata.qid_others_service import (
    get_title_to_qid as get_others_qids,
    update_qid_by_value as update_others_qid_by_value,
    batch_upsert_qids as batch_upsert_others_qids,
)
from md_core.unlinked_wb.bot import work_un
from md_core_helps.apis import cat_cach, wikidataapi
from md_core_helps.bots.check_title import valid_title

logger = logging.getLogger(__name__)

all_pages = cat_cach.from_cache()
all_pages = [x for x in all_pages[:] if valid_title(x)]


def replace_in_sql(reds, ty) -> None:
    # ---
    table_name = "qids_others" if ty == "other" else "qids"
    # ---
    for numb, (old_q, new_q) in enumerate(reds.items(), start=1):
        # ---
        logger.info(f"<<blue>> {numb}, old_q: {old_q}, new_q: {new_q}")
        # ---
        qua = f'update {table_name} set qid = "{new_q}" where qid = "{old_q}"'
        # ---
        if "fix" in sys.argv:
            # python3 core8/pwb.py md_core/mdpy/cashwd redirects fix
            if table_name == "qids_others":
                update_others_qid_by_value(old_q, new_q)
            else:
                update_qid_by_value(old_q, new_q)
        else:
            logger.info(qua)
            logger.info('<<green>> add "fix" to sys.argv to fix them..')


def get_redirects(to_work):
    # ---
    logger.info("<<yellow>> start ()")
    # ---
    new_list = list(to_work.keys())
    # ---
    logger.info(f"<<yellow>> start (), {len(new_list)=}")
    # ---
    reds = wikidataapi.get_redirects(new_list)
    # ---
    return reds


def add_to_qids(sql_results_qids, ty) -> None:
    # ---
    logger.info(f"<<yellow>> start ({ty=})")
    # ---
    all_in = list(sql_results_qids)
    # ---
    new_list = {title: "" for title in all_pages if title not in all_in}
    # ---
    logger.info(f"len of new_list: {len(new_list)}")
    # ---
    if not new_list:
        logger.info("<<red>> new_list empty.. exit()..")
        return
    # ---
    if ty == "other":
        batch_upsert_others_qids(new_list, add_empty_qid=True)
    else:
        batch_upsert_qids(new_list, add_empty_qid=True)


def do(ty) -> None:
    # ---
    if ty == "other":
        sql_results_qids = get_others_qids()
    else:
        sql_results_qids = get_title_to_qid()
    # ---
    to_work = {q: t for t, q in sql_results_qids.items() if q != ""}
    # ---
    p_reds = get_redirects(to_work)
    # ---
    reds = {o_q: n_q for o_q, n_q in p_reds.items() if n_q != o_q}
    # ---
    logger.info(f"len of redirects: {len(p_reds)}, len of reds after remove the sames: {len(reds)}")
    # ---
    if reds:
        logger.info(f'<<green>> {len(reds)=} add "fix" to sys.argv to fix them..')
        replace_in_sql(reds, ty)
    # ----
    tab = {to_work.get(old_q): new_q for old_q, new_q in reds.items() if to_work.get(old_q)}
    # ----
    work_un(tab)
    # ---
    logger.info("_______________")
    # ---
    add_to_qids(sql_results_qids, ty)


def start() -> None:
    # ---
    tys = ["td"]
    # ---
    if "all" in sys.argv:
        tys = ["td", "other"]
    # ---
    if "-others" in sys.argv:
        tys = ["other"]
    # ---
    for ty in tys:
        do(ty)


if __name__ == "__main__":
    start()
