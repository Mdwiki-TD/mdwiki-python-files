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

# ---
from mdpy.bots import en_to_md
# en_to_md.mdtitle_to_qid
# en_to_md.enwiki_to_mdwiki
# en_to_md.mdwiki_to_enwiki
# ---

"""

import json
import logging
import os

from mdapi_sql import sql_for_mdwiki

logger = logging.getLogger(__name__)


# ---
if os.getenv("HOME"):
    public_html_dir = os.getenv("HOME") + "/public_html"
else:
    public_html_dir = "I:/mdwiki/mdwiki/public_html"
# ---
enwiki_to_mdwiki = {}
mdwiki_to_enwiki = {}
# ---
mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# ---
lala = ""


def make_mdwiki_list():
    # ---
    ffile = f"{public_html_dir}/td/Tables/jsons/medwiki_to_enwiki.json"
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
