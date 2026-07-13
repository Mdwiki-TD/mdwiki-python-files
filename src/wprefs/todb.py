import json
import logging
import os
from pathlib import Path

from db.mdapi_sql import sql_for_mdwiki

logger = logging.getLogger(__name__)


Dir = Path(__file__).parents[0]
# ---
dir2 = os.getenv("HOME")
# ---
if not dir2:
    dir2 = "I:/MD_TOOLS/MDWIKI_MAIN_REPO"
# ---
fixwikirefs = dir2 + "/confs/fixwikirefs.json"
# ---

with open(fixwikirefs, "r", encoding="utf-8") as f:
    data = json.load(f)

CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS language_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lang_code VARCHAR(20) UNIQUE,
    move_dots TINYINT DEFAULT 0,
    expend TINYINT DEFAULT 0,
    add_en_lang TINYINT DEFAULT 0
)
"""

sql_for_mdwiki.mdwiki_sql(CREATE_TABLE)

# sort data by key
data = dict(sorted(data.items()))

for n, (lang_code, settings) in enumerate(data.items()):
    move_dots = settings.get("move_dots", 0)
    expend = settings.get("expend", 0)
    add_en_lang = settings.get("add_en_lang", 0)
    # ---
    query = "INSERT INTO language_settings (lang_code, move_dots, expend, add_en_lang) VALUES (%s, %s, %s, %s)"
    # ---
    params = [lang_code, move_dots, expend, add_en_lang]
    # ---
    logger.info(f"lang {n}/{len(data)}:{lang_code=}")
    # ---
    sql_for_mdwiki.mdwiki_sql(query, values=params)
