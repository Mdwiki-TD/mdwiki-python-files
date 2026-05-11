"""
python3 core8/pwb.py mdpy/bots/tests/test_sql_for_mdwiki
"""

import json
import logging

from mdapi_sql import sql_for_mdwiki

logger = logging.getLogger(__name__)


def tests():
    # ---
    # test_get_all_qids
    # return
    # test_get_all_pages
    # pages = select_md_sql(' select DISTINCT * from pages limit 10;', return_dict=True)
    pages = sql_for_mdwiki.get_all_pages_all_keys(lang="ar", table="pages_users")
    logger.info(f"<<yellow>> len of pages:{len(pages)}")
    for x in pages:
        # logger.info(type(x['add_date']))
        # logger.info(x)
        logger.info(json.dumps(x, indent=2))
        # logger.info(x['add_date'])
    # logger.info()

    # ---


if __name__ == "__main__":
    tests()
