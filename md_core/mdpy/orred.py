#!/usr/bin/python3
"""

إنشاء تحويلات من العنوان الإنجليزي
إلى العنوان المحلي
في orwiki

python3 core8/pwb.py mdpy/orred

"""
from mdapi_sql import sql_for_mdwiki
from newapi import printe
from newapi.wiki_page import NEW_API, MainPage

api_new = NEW_API("or", family="wikipedia")


def create_redirect(target, mdtitle):
    # ---
    if not target or not mdtitle:
        printe.output(f"<<red>>** false .. {mdtitle=} | {target=} ")
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
            printe.output(f"<<green>>** true .. [[or:{mdtitle}]] ")


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
    printe.output("<<yellow>> check targets")
    # ---
    pages, p_not_exists = check_all(list(targets_to_titles.keys()))
    # ---
    targets_exists = {x: targets_to_titles.get(x) for x in pages}
    # ---
    mdtitle_exists, c_not_exists = check_all(list(targets_exists.values()))
    # ---
    printe.output(f"<<yellow>> check targets({len(targets_to_titles)}) exists:{len(pages):,} not_exists:{len(p_not_exists):,}")
    # ---
    printe.output(f"<<yellow>> check mdwikis({len(targets_exists)}) exists:{len(mdtitle_exists):,} not_exists:{len(c_not_exists):,}")
    # ---
    to_work = {x: v for x, v in targets_exists.items() if v in c_not_exists}
    # ---
    for n, (target, mdtitle) in enumerate(to_work.items(), start=1):
        # ---
        printe.output(f"----------\n*<<yellow>> p{n}/{len(to_work)} >{target=}, {mdtitle=}.")
        # ---
        create_redirect(target, mdtitle)


if __name__ == "__main__":
    start()
