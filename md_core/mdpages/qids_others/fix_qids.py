#!/usr/bin/env python
#   himo
"""
python3 core8/pwb.py qids_others/qids_others/fix_qids

"""
import sys
from mdpy.bots import wikidataapi
from mdpy import printe
from mdpy.bots import sql_for_mdwiki
from mdpy.bots import sql_qids_others
from unlinked_wb.bot import work_un
# ---
qids_othrs = sql_qids_others.get_others_qids()
# ---
qids_to_title = {q: t for t, q in qids_othrs.items()}
# ---
to_work = [q for q in qids_othrs.values() if q != '']


def fix_redirects():
    # ---
    printe.output('<<lightyellow>> start fix_redirects()')
    # ---
    new_list = to_work
    # ---
    reds = wikidataapi.get_redirects(new_list)
    # ---
    printe.output(f'len of redirects: {len(reds)}')
    # ---
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
    # ----
    tab = {qids_to_title.get(old_q) : new_q for old_q, new_q in reds.items() if qids_to_title.get(old_q) }
    # ----
    work_un(tab)


if __name__ == '__main__':
    fix_redirects()
