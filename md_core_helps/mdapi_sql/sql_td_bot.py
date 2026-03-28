#!/usr/bin/python3
"""

"""
import logging
import os
import sys
import pymysql
from pywikibot import config
import copy
import pymysql.cursors

logger = logging.getLogger(__name__)

conversions = pymysql.converters.conversions
conversions[pymysql.FIELD_TYPE.DATE] = lambda x: str(x)

db_username = config.db_username
db_password = config.db_password
# ---
if config.db_connect_file is None:
    credentials = {"user": db_username, "password": db_password}
else:
    credentials = {"read_default_file": config.db_connect_file}
    # read default fil
    db_username = os.getenv("TOOL_TOOLSDB_USER")
# ---
main_args = {
    "host": "tools.db.svc.wikimedia.cloud",
    "db": f"{db_username}__mdwiki",
    "charset": "utf8mb4",
    # 'collation':  'utf8_general_ci',
    "use_unicode": True,
    "autocommit": True,
}
# ---
main_args_new = main_args.copy()
main_args_new["db"] = f"{db_username}__mdwiki_new"
# ---
# if "localhost" in sys.argv or dir2 == "I:/mdwiki":
if "localhost" in sys.argv or not os.getenv("HOME"):
    credentials = {"user": "root", "password": "root11"}
    main_args["host"] = "127.0.0.1"
    main_args_new["host"] = "127.0.0.1"
    main_args["db"] = f"{db_username}__mdwiki"
    main_args_new["db"] = f"{db_username}__mdwiki_new"
    logger.info("sql_td_bot localhost")


def _sql_connect_pymysql(
    query,
    return_dict=False,
    values=None,
    main_args={},
    credentials={},
    conversions=None,
    many=False,
    **kwargs,
):
    args = copy.deepcopy(main_args)
    args["cursorclass"] = pymysql.cursors.DictCursor if return_dict else pymysql.cursors.Cursor
    if conversions:
        args["conv"] = conversions

    params = values or None  # Simplify condition

    try:
        connection = pymysql.connect(**args, **credentials)
    except Exception as e:
        logger.exception(e)
        return []

    with connection as conn, conn.cursor() as cursor:
        # skip sql errors
        try:
            if many:
                cursor.executemany(query, params)
            else:
                cursor.execute(query, params)

        except Exception as e:
            logger.exception(e)
            return []

        try:
            results = cursor.fetchall()
        except Exception as e:
            logger.exception(e)
            logger.exception('Exception during fetchall', exc_info=True)
            return []

    return results


def sql_connect_pymysql(query, return_dict=False, values=None, many=False, **kwargs):
    # ---
    results = _sql_connect_pymysql(
        query,
        return_dict=return_dict,
        values=values,
        main_args=main_args,
        credentials=credentials,
        conversions=conversions,
        many=many,
        **kwargs,
    )
    # ---
    return results
