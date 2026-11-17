#!/usr/bin/python3
"""

python3 c9/pwb.py apis/cat_cach

from md_core_helps.apis import cat_cach
from md_core_helps.apis.cat_cach import cat_depth
all_pages = cat_cach.from_cache()

USED IN mdwiki-jobs.yaml
"""

import logging
import time
from datetime import datetime

from db.mdapi_sql.services import sql_for_mdwiki
from md_core_helps.bots.check_title import valid_title
from mdwiki_api.mdwiki_page import CatDepth

logger = logging.getLogger(__name__)

today = datetime.today().strftime("%Y-%m-%d")


def make_cash_to_cats(dump_data: bool = False) -> list[str]:

    all_pages = []

    cats = sql_for_mdwiki.get_db_categories()

    all_cats = {}

    for cat, depth in cats.items():
        ca = cat_depth(cat, depth=depth, ns="all", print_s=False)

        all_cats[cat] = ca

        all_pages.extend([x for x in ca if x not in all_pages])

    return all_pages


def from_cache() -> list[str]:
    all_pages = make_cash_to_cats()
    return all_pages


def cat_depth(title, depth: int = 0, ns: str = "all", print_s: bool = True) -> list[str]:

    if not title.startswith("Category:"):
        title = "Category:" + title

    start = time.time()

    result_table = CatDepth(title, sitecode="www", family="mdwiki", depth=0, ns="all", print_s=print_s, gcmlimit="max")

    # result_table = {key: result_table[key] for key in result_table if valid_title(key)}
    result_table = dict(filter(lambda item: valid_title(item[0]), result_table.items()))

    final = time.time()

    delta = final - start

    delta = round(delta, 5)

    logger.info(
        f"<<blue>>CatDepth result<<yellow>> ({len(result_table)}) ns:{ns} in {title}, depth:{depth} in {delta} seconds"
    )

    return list(result_table.keys())
