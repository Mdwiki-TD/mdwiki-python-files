#!/usr/bin/python3
"""

python3 core8/pwb.py mdpy/copy_qids

delete from qids q1 WHERE (q1.qid = '' OR q1.qid IS NULL) and EXISTS (SELECT 1 FROM qids q2 WHERE q1.title = q2.title and q2.qid != '')

"""

import sys
from pathlib import Path

from mdapi_sql import sql_for_mdwiki
from mdpy.bots import en_to_md

in_qids = sql_for_mdwiki.get_all_qids()
# ---
len_qids_empty = len([x for x in in_qids if in_qids[x].find("Q") == -1])
len_qids_not_empty = len([x for x in in_qids if in_qids[x] != ""])
# ---
logger.info(f"len_qids_empty = {len_qids_empty}")
logger.info(f"len_qids_not_empty = {len_qids_not_empty}")
# ---

Dir = str(Path(__file__).parents[0])

qids_list = en_to_md.mdtitle_to_qid
# ---
num = 0
# ---
all_texts = ""
texts = ""
# ---
logger.info(f"len(qids_list) = {len(qids_list)}")
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
            logger.info(texts)
            texts = ""
# ---
if texts != "":
    logger.info(texts)
    vfg = sql_for_mdwiki.mdwiki_sql(texts, update=True)
# ---
# log all_texts
with open(f"{Dir}/copy_qids.txt", "w", encoding="utf-8") as f:
    f.write(all_texts)
# ---
