#!/usr/bin/python3
"""

python3 core8/pwb.py md_core/mdpy/copy_qids

delete from qids q1 WHERE (q1.qid = '' OR q1.qid IS NULL) and EXISTS (SELECT 1 FROM qids q2 WHERE q1.title = q2.title and q2.qid != '')

"""

import logging
from pathlib import Path

from sqlalchemy import text

from db.tools.services.session import get_session
from db.tools.services.wikidata import qid_service
from md_core_helps.bots import en_to_md

logger = logging.getLogger(__name__)


in_qids = qid_service.get_title_to_qid()
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
with get_session() as session:
    for title, qid in qids_list.items():
        # ---
        qid_in = in_qids.get(title, "")
        # ---
        if title in in_qids:
            if qid != qid_in:
                session.execute(text("UPDATE qids SET qid = :qid WHERE title = :title"), {"title": title, "qid": qid})
            else:
                continue
            qua = "UPDATE qids set qid = %s where title = %s;"
        else:
            session.execute(text("INSERT INTO qids (title, qid) VALUES (:title, :qid)"), {"title": title, "qid": qid})
            qua = "INSERT INTO qids (title, qid) SELECT %s, %s;"
        # ---
        num += 1
        # ---
        all_texts += f"\n{qua}"
        texts += f"\n{qua}"
        # ---
        if num % 300 == 0:
            if texts != "":
                logger.info(texts)
                texts = ""
# ---
if texts != "":
    logger.info(texts)
# ---
# log all_texts
with open(f"{Dir}/copy_qids.txt", "w", encoding="utf-8") as f:
    f.write(all_texts)
# ---
