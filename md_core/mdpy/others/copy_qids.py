#!/usr/bin/python3
"""

python3 core8/pwb.py mdpy/copy_qids

delete from qids q1 WHERE q1.qid = '' and EXISTS  (SELECT 1 FROM qids q2 WHERE q1.title = q2.title and q2.qid != '')

"""

import sys
from pathlib import Path
from mdpy.bots import en_to_md

from mdapi_sql import sql_for_mdwiki

in_qids = sql_for_mdwiki.get_all_qids()
# ---
len_qids_empty = len([x for x in in_qids if in_qids[x].find("Q") == -1])
len_qids_not_empty = len([x for x in in_qids if in_qids[x] != ""])
# ---
print(f"len_qids_empty = {len_qids_empty}")
print(f"len_qids_not_empty = {len_qids_not_empty}")
# ---

Dir = str(Path(__file__).parents[0])

qids_list = en_to_md.mdtitle_to_qid
# ---
num = 0
# ---
all_texts = ""
texts = ""
# ---
print(f"len(qids_list) = {len(qids_list)}")
# ---
for title, qid in qids_list.items():
    # ---
    qid_in = in_qids.get(title, "")
    # ---
    qua = "INSERT INTO qids (title, qid) SELECT %s, %s;"
    # ---
    values = [title, qid]
    # ---
    if title in in_qids:
        qua = "UPDATE qids set qid = %s where title = %s;"
        values = [qid, title]
        if qid == qid_in:
            qua = ""
    # ---
    if qua != "":
        num += 1
        # ---
        all_texts += f"\n{qua}"
        texts += f"\n{qua}"
        # ---
        vfg = sql_for_mdwiki.mdwiki_sql(texts, update=True, values=values)
    # ---
    if num % 300 == 0:
        if texts != "":
            print(texts)
            texts = ""
# ---
if texts != "":
    print(texts)
    vfg = sql_for_mdwiki.mdwiki_sql(texts, update=True)
# ---
# log all_texts
with open(f"{Dir}/copy_qids.txt", "w", encoding="utf-8") as f:
    f.write(all_texts)
# ---
