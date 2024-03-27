#!/usr/bin/env python
#   himo
"""
python3 core8/pwb.py mdpages/fixqids_others

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
        qua = f'update qids_others set qid = "{new_q}" where qid = "{old_q}"'
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


def start():
    # ---
    sql_qids = sql_qids_others.get_others_qids()
    # ---
    to_work = {q: t for t, q in sql_qids.items() if q != ''}
    # ---
    fix_redirects(to_work)
    print('_______________d')
    print('_______________d')
    print('_______________d')
    # add_to_qids(sql_qids)


if __name__ == '__main__':
    start()
