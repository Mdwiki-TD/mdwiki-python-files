"""
python3 core8/pwb.py td_other_qids/fix_qids all
python3 core8/pwb.py td_other_qids/fix_qids -others
python3 core8/pwb.py td_other_qids/fix_qids td
python3 core8/pwb.py td_other_qids/fix_qids redirects

"""
import sys

from apis import cat_cach
from apis import wikidataapi
from newapi import printe
from mdpy.bots.check_title import valid_title
from mdapi_sql import sql_for_mdwiki
from mdapi_sql import sql_qids_others
from unlinked_wb.bot import work_un

all_pages = cat_cach.from_cache()
all_pages = [x for x in all_pages[:] if valid_title(x)]


def replace_in_sql(reds, ty):
    # ---
    table_name = "qids_others" if ty == "other" else "qids"
    # ---
    for numb, (old_q, new_q) in enumerate(reds.items(), start=1):
        # ---
        printe.output(f"<<blue>> {numb}, old_q: {old_q}, new_q: {new_q}")
        # ---
        qua = f'update {table_name} set qid = "{new_q}" where qid = "{old_q}"'
        # ---
        if "fix" in sys.argv:
            # python3 core8/pwb.py mdpy/cashwd redirects fix
            if table_name == "qids_others":
                sql_qids_others.set_qid_where_qid(new_q, old_q)
            else:
                sql_for_mdwiki.set_qid_where_qid(new_q, old_q)
        else:
            printe.output(qua)
            printe.output('<<green>> add "fix" to sys.argv to fix them..')


def get_redirects(to_work):
    # ---
    printe.output("<<yellow>> start get_redirects()")
    # ---
    new_list = list(to_work.keys())
    # ---
    printe.output(f"<<yellow>> start get_redirects(), {len(new_list)=}")
    # ---
    reds = wikidataapi.get_redirects(new_list)
    # ---
    return reds


def add_to_qids(sql_qids, ty):
    # ---
    printe.output(f"<<yellow>> start add_to_qids({ty=})")
    # ---
    all_in = list(sql_qids)
    # ---
    new_list = {title: "" for title in all_pages if title not in all_in}
    # ---
    printe.output(f"len of new_list: {len(new_list)}")
    # ---
    if not new_list:
        printe.output("<<red>> new_list empty.. exit()..")
        return
    # ---
    sql_for_mdwiki.add_titles_to_qids(new_list, add_empty_qid=True)


def do(ty):
    # ---
    if ty == "other":
        sql_qids = sql_qids_others.get_others_qids()
    else:
        sql_qids = sql_for_mdwiki.get_all_qids()
    # ---
    to_work = {q: t for t, q in sql_qids.items() if q != ""}
    # ---
    p_reds = get_redirects(to_work)
    # ---
    reds = {o_q: n_q for o_q, n_q in p_reds.items() if n_q != o_q}
    # ---
    printe.output(f"len of redirects: {len(p_reds)}, len of reds after remove the sames: {len(reds)}")
    # ---
    if reds:
        printe.output(f'<<green>> {len(reds)=} add "fix" to sys.argv to fix them..')
        replace_in_sql(reds, ty)
    # ----
    tab = {to_work.get(old_q): new_q for old_q, new_q in reds.items() if to_work.get(old_q)}
    # ----
    work_un(tab)
    # ---
    print("_______________")
    # ---
    add_to_qids(sql_qids, ty)


def start():
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
