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
    """
    qua = ' select DISTINCT * from pages where lang ="zh" limit 100;'
    # ---
    qids = sql_connect_pymysql(qua)
    print('sql_connect_pymysql:')
    print(len(qids))
    # ---
    # test_add_qid
    a = add_qid('test', 'test')
    logger.info(f'<<yellow>> add: {a}')
    aa = add_qid('test11', '11')
    logger.info(f'<<yellow>> add: {aa}')
    # ---
    # test_update_qid
    zz = set_qid_where_title('test11', 'xxx')
    logger.info(f'<<yellow>> update: {zz}')
    # ---
    """
    # return
    # test_get_all_pages
    # pages = select_md_sql(' select DISTINCT * from pages limit 10;', return_dict=True)
    pages = sql_for_mdwiki.get_all_pages_all_keys(lang="ar", table="pages_users")
    logger.info(f"<<yellow>> len of pages:{len(pages)}")
    for x in pages:
        # print(type(x['add_date']))
        # print(x)
        print(json.dumps(x, indent=2))
        # print(x['add_date'])
    # logger.info()

    # ---


if __name__ == "__main__":
    tests()
