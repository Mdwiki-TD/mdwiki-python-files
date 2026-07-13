"""
python3 core8/pwb.py md_core/stats/qids ask

from md_core.stats.qids import qids_list

"""

import json
import logging
import os
from pathlib import Path

from db import WikiReplicaDB

logger = logging.getLogger(__name__)


Dir = Path(__file__).parent

qids_file = Dir / "qids.json"

if not os.path.exists(qids_file):
    with open(qids_file, "w", encoding="utf-8") as f:
        json.dump({}, f, sort_keys=True)

qids_list = {}

with open(qids_file, "r", encoding="utf-8") as f:
    qids_list = json.load(f)


def get_en_articles():
    # ---
    query = """
    SELECT p.page_title, pp_value
        FROM page p, categorylinks, page_props, page p2
        WHERE p.page_id = cl_from
        AND cl_to = 'All_WikiProject_Medicine_pages'
        # AND cl_to = 'All_WikiProject_Medicine_articles'
        AND p.page_namespace = 1
        AND p2.page_namespace = 0
        AND pp_propname = 'wikibase_item'
        and p.page_title = p2.page_title
        and pp_page = p2.page_id
    """
    # ---
    lang_db = WikiReplicaDB("enwiki")
    result = lang_db.select_safe(query)
    return {x["page_title"]: x["pp_value"] for x in result}


def start() -> None:
    # ---
    articles = get_en_articles()
    # ---
    logger.info(f"len articles: {len(articles)}")
    # ---
    qids_list = list(articles.values())
    # ---
    # dump
    with open(qids_file, "w", encoding="utf-8") as f:
        json.dump(qids_list, f, sort_keys=True)


if __name__ == "__main__":
    start()
