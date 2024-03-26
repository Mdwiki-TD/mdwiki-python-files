#!/usr/bin/env python
#   himo
"""
python3 core8/pwb.py mdpy/fixqids
python3 core8/pwb.py mdpy/fixqids redirects

"""
import sys
from mdpy.bots import catdepth2
from mdpy.bots import wikidataapi
from mdpy import printe
from mdpy.bots.check_title import valid_title
from mdpy.bots import sql_for_mdwiki
from mdpy.bots import sql_qids_others
from unlinked_wb.bot import work_un


def replace_in_sql(reds):
    for numb, (old_q, new_q) in enumerate(reds.items(), start=1):
        # ---
        printe.output(f'<<lightblue>> {numb}, old_q: {old_q}, new_q: {new_q}')
        # ---
        qua = f'update qids set qid = "{new_q}" where qid = "{old_q}"'
        # ---
        if 'fix' in sys.argv:
            # python3 core8/pwb.py mdpy/cashwd redirects fix
            sql_for_mdwiki.mdwiki_sql(qua, update=True)
        else:
            printe.output(qua)
            printe.output('<<lightgreen>> add "fix" to sys.argv to fix them..')


def fix_redirects(to_work):
    # ---
    printe.output('<<lightyellow>> start fix_redirects()')
    # ---
    new_list = list(to_work.keys())
    # ---
    reds = wikidataapi.get_redirects(new_list)
    # ---
    printe.output(f'len of redirects: {len(reds)}')
    # ---
    if reds:
        printe.output('<<lightgreen>> add "fix" to sys.argv to fix them..')
        # ---
        replace_in_sql(reds)
    # ----
    tab = {to_work.get(old_q) : new_q for old_q, new_q in reds.items() if to_work.get(old_q) }
    # ----
    work_un(tab)


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


def start():
    # ---
    sql_qids = sql_for_mdwiki.get_all_qids()
    # ---
    to_work = {q: t for t, q in sql_qids.items() if q != ''}
    # ---
    fix_redirects(to_work)
    print('_______________d')
    print('_______________d')
    print('_______________d')
    add_to_qids(sql_qids)


if __name__ == '__main__':
    start()
