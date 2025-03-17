"""
Usage:

python3 core8/pwb.py p11143_bot/bot -others
python3 core8/pwb.py p11143_bot/bot -td

"""
import sys

from mdapi_sql import sql_for_mdwiki
from mdapi_sql import sql_qids_others
from newapi import printe
from apis import cat_cach
from p11143_bot.wd_helps import fix_in_wd, add_P11143_to_qids_in_wd, make_in_wd_tab
from p11143_bot.filter_helps import remove_in_db_elements

TD_list = cat_cach.from_cache()

ALL_QIDS = {}


def duplicate(merge_qids):
    # ايجاد عناصر ويكي بيانات بها قيمة الخاصية في أكثر من عنصر
    va_tab = {}
    # ---
    for q, va in merge_qids.items():
        # ---
        if va not in va_tab:
            va_tab[va] = []
        # ---
        if q not in va_tab[va]:
            va_tab[va].append(q)
    # ---
    va_tab_x = {k: v for k, v in va_tab.items() if len(v) > 1}
    # ---
    if va_tab_x:
        printe.output(f"<<yellow>> len of va_tab_x: {len(va_tab_x)}")
        # ---
        for va, qs in va_tab_x.items():
            printe.output(f"va:{va}, qs:{qs}")
    # ---
    printe.output("<<yellow>> duplicate() end...")


def add_q(new_qids, ty):
    # ---
    printe.output(f"len of new_qids: {len(new_qids)}")
    # ---
    if len(new_qids) == 0:
        return
    # ---
    new_qids = remove_in_db_elements(new_qids, ALL_QIDS["other"], ALL_QIDS["td"])
    # ---
    if len(new_qids) < 10:
        printe.output("\n".join([f"{k}:{v}" for k, v in new_qids.items()]))
    # ---
    newtitles_not_td = {title: qid for qid, title in new_qids.items() if title not in TD_list}
    newtitles_in_td = {title: qid for qid, title in new_qids.items() if title in TD_list}
    # ---
    printe.output(f"<<yellow>> add_q: {len(newtitles_in_td)=}, {len(newtitles_not_td)=}")
    # ---
    if not newtitles_in_td and not newtitles_not_td:
        return
    # ---
    printe.output('<<puruple>> add "addq" to sys.argv to add them to qids')
    # ---
    if newtitles_in_td:
        printe.output("<<yellow>> sql_for_mdwiki.add_titles_to_qids(newtitles_in_td):")
        for title, qid in newtitles_in_td.items():
            printe.output(f"\t add {title} to qid {qid}")
    # ---
    if newtitles_in_td:
        printe.output("<<yellow>> sql_qids_others.add_titles_to_qids(newtitles_not_td):")
        # ---
        for title, qid in newtitles_not_td.items():
            printe.output(f"\t add {title} to qid {qid}")
    # ---
    printe.output('<<puruple>> add "addq" to sys.argv to add them to qids')
    # ---
    if "addq" in sys.argv:
        sql_for_mdwiki.add_titles_to_qids(newtitles_in_td)
        # ---
        sql_qids_others.add_titles_to_qids(newtitles_not_td)


def work_qids(ty):
    # ---
    qids_list = ALL_QIDS[ty]
    # ---
    in_wd = make_in_wd_tab()
    # ---
    printe.output(f"len of in_wd: {len(in_wd)}")
    # ---
    if not in_wd:
        return
    # ---
    qids = {q: title for title, q in qids_list.items() if q != ""}
    # ---
    new_qids = {q: p for q, p in in_wd.items() if q not in qids.keys() and p not in qids.values()}
    # ---
    newlist = {q: tt for q, tt in qids.items() if q not in in_wd.keys()}
    # ---
    add_P11143_to_qids_in_wd(newlist)
    # ---
    merge_qids = newlist | in_wd
    # ---
    if "fix" in sys.argv:
        fix_in_wd(merge_qids, qids)
    # ---
    duplicate(merge_qids)
    # ---
    add_q(new_qids, ty)


def start():
    # ---
    ALL_QIDS["other"] = sql_qids_others.get_others_qids()
    ALL_QIDS["td"] = sql_for_mdwiki.get_all_qids()
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
        work_qids(ty)


if __name__ == "__main__":
    start()
