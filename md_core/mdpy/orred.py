#!/usr/bin/python3
"""

إنشاء تحويلات من العنوان الإنجليزي
إلى العنوان المحلي
في orwiki

python3 core8/pwb.py mdpy/orred

"""
import logging

from mdapi_sql import sql_for_mdwiki
from newapi.wiki_page import NEW_API, MainPage

logger = logging.getLogger(__name__)

api_new = NEW_API("or", family="wikipedia")


def create_redirect(target, mdtitle):
    # ---
    if not target or not mdtitle:
        logger.info(f"<<red>>** false .. {mdtitle=} | {target=} ")
        return
    # ---
    text = f"#redirect [[{target}]]"
    sus = f"Redirected page to [[{target}]]"
    # ---
    page = MainPage(mdtitle, "or", family="wikipedia")
    # ---
    if not page.exists():
        create = page.Create(text=text, summary=sus)
        # ---
        if create:
            logger.info(f"<<green>>** true .. [[or:{mdtitle}]] ")


def check_all(links):
    # ---
    check_it = api_new.Find_pages_exists_or_not(links, get_redirect=False)
    # ---
    exists = [x for x in check_it.keys() if check_it[x]]
    # ---
    not_exists = [x for x in check_it.keys() if not check_it[x]]
    # ---
    return exists, not_exists


def start():
    # ---
    que = """select title, target from pages where target != "" and lang = "or";"""
    # ---
    sq = sql_for_mdwiki.select_md_sql(que, return_dict=True)
    # ---
    targets_to_titles = {}
    # ---
    for _, tab in enumerate(sq, start=1):
        mdtitle = tab["title"]
        target = tab["target"]
        # ---
        targets_to_titles[target] = mdtitle
    # ---
    logger.info("<<yellow>> check targets")
    # ---
    pages, p_not_exists = check_all(list(targets_to_titles.keys()))
    # ---
    targets_exists = {x: targets_to_titles.get(x) for x in pages}
    # ---
    mdtitle_exists, c_not_exists = check_all(list(targets_exists.values()))
    # ---
    logger.info(
        f"<<yellow>> check targets({len(targets_to_titles)}) exists:{len(pages):,} not_exists:{len(p_not_exists):,}"
    )
    # ---
    logger.info(
        f"<<yellow>> check mdwikis({len(targets_exists)}) exists:{len(mdtitle_exists):,} not_exists:{len(c_not_exists):,}"
    )
    # ---
    to_work = {x: v for x, v in targets_exists.items() if v in c_not_exists}
    # ---
    for n, (target, mdtitle) in enumerate(to_work.items(), start=1):
        # ---
        logger.info(f"----------\n*<<yellow>> p{n}/{len(to_work)} >{target=}, {mdtitle=}.")
        # ---
        create_redirect(target, mdtitle)


if __name__ == "__main__":
    start()
