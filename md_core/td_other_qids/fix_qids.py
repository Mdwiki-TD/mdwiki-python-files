"""
python3 core8/pwb.py td_other_qids/fix_qids all
python3 core8/pwb.py td_other_qids/fix_qids -others
python3 core8/pwb.py td_other_qids/fix_qids td
python3 core8/pwb.py td_other_qids/fix_qids redirects

"""
import sys
from apis import catdepth2
from apis import wikidataapi
from newapi import printe
from mdpy.bots.check_title import valid_title
from api_sql import sql_for_mdwiki
from api_sql import sql_qids_others
from unlinked_wb.bot import work_un


def replace_in_sql(reds, ty):
    # ---
    table_name = "qids_others" if ty == "other" else "qids"
    # ---
    for numb, (old_q, new_q) in enumerate(reds.items(), start=1):
        # ---
        printe.output(f'<<lightblue>> {numb}, old_q: {old_q}, new_q: {new_q}')
        # ---
        qua = f'update {table_name} set qid = "{new_q}" where qid = "{old_q}"'
        # ---
        if 'fix' in sys.argv:
            # python3 core8/pwb.py mdpy/cashwd redirects fix
            sql_for_mdwiki.mdwiki_sql(qua, update=True)
        else:
            printe.output(qua)
            printe.output('<<lightgreen>> add "fix" to sys.argv to fix them..')


def get_redirects(to_work):
    # ---
    printe.output('<<lightyellow>> start get_redirects()')
    # ---
    new_list = list(to_work.keys())
    # ---
    printe.output(f'<<lightyellow>> start get_redirects(), {len(new_list)=}')
    # ---
    reds = wikidataapi.get_redirects(new_list)
    # ---
    return reds


def add_to_qids(sql_qids):
    # ---
    printe.output('<<lightyellow>> start add_to_qids()')
    # ---
    all_pages = catdepth2.make_cash_to_cats(return_all_pages=True)
    # ---
    all_pages = [x for x in all_pages[:] if valid_title(x)]
    # ---
    all_in = list(sql_qids)
    # ---
    new_list = {title: '' for title in all_pages if title not in all_in}
    # ---
    printe.output(f'len of new_list: {len(new_list)}')
    # ---
    sql_for_mdwiki.add_titles_to_qids(new_list, add_empty_qid=True)


def do(ty):
    # ---
    if ty == "other":
        sql_qids = sql_qids_others.get_others_qids()
    else:
        sql_qids = sql_for_mdwiki.get_all_qids()
    # ---
    to_work = {q: t for t, q in sql_qids.items() if q != ''}
    # ---
    p_reds = get_redirects(to_work)
    # ---
    reds = {o_q: n_q for o_q, n_q in p_reds.items() if n_q != o_q}
    # ---
    printe.output(f'len of redirects: {len(p_reds)}, len of reds after remove the sames: {len(reds)}')
    # ---
    if reds:
        printe.output(f'<<lightgreen>> {len(reds)=} add "fix" to sys.argv to fix them..')
        replace_in_sql(reds, ty)
    # ----
    tab = {to_work.get(old_q) : new_q for old_q, new_q in reds.items() if to_work.get(old_q) }
    # ----
    work_un(tab)
    # ---
    print('_______________')
    # ---
    add_to_qids(sql_qids)


def start():
    # ---
    if "all" in sys.argv:
        do("td")
        do("other")
        exit()
    # ---
    ty = "other" if "-others" in sys.argv else "td"
    # ---
    do(ty)

if __name__ == "__main__":
    start()
