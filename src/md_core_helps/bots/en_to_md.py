"""
11p deletion syndrome
Vulvar pain
Diabetic foot infection
Kidney agenesis
Orbital compartment syndrome
Pelvic floor disorders
Perianal itching
Genital itch
Lateral canthotomy
Prostate abscess

# Etonogestrel موجودة في ويكي إنجليزية تحويلة إلى المقالة الهدف الموجودة في ويكي ميد

"""

import json
import logging

from db.mdapi_sql import sql_qids
from td_core.td_dirs import paths

logger = logging.getLogger(__name__)

enwiki_to_mdwiki = {}
mdwiki_to_enwiki = {}
# ---
mdtitle_to_qid = sql_qids.get_all_qids()
# ---
lala = ""


def make_mdwiki_list() -> None:
    # ---
    ffile = paths.json_files.medwiki_to_enwiki
    # ---
    From_json = {}
    # ---
    # read the file without errors
    try:
        From_json = json.loads(open(ffile, "r", encoding="utf-8-sig").read())
    except Exception as e:
        logger.info(e)
        return
    # ---
    for md, en in From_json.items():
        enwiki_to_mdwiki[en] = md
        mdwiki_to_enwiki[md] = en


make_mdwiki_list()
