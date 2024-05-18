'''

from stats.qids import qids_list

'''
import json
import os
import sys
from pathlib import Path
from api_sql import wiki_sql

Dir = Path(__file__).parent

qids_file = Dir / 'qids.json'

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
        AND cl_to = 'All_WikiProject_Medicine_articles'
        AND p.page_namespace = 1
        AND p2.page_namespace = 0
        AND pp_propname = 'wikibase_item'
        and p.page_title = p2.page_title
        and pp_page = p2.page_id
    """
    # ---
    result = wiki_sql.sql_new(query, 'enwiki')
    return {x['page_title']: x['pp_value'] for x in result}


def start():
    # ---
    articles = get_en_articles()
    # ---
    qids_list = list(articles.values())
    # ---
    # dump
    with open(qids_file, "w", encoding="utf-8") as f:
        json.dump(qids_list, f, sort_keys=True)


if __name__ == "__main__":
    start()
