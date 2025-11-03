#!/usr/bin/python3
"""
# ---
from mdapi_sql import sql_td_bot
# result = sql_td_bot.sql_connect_pymysql(query, return_dict=return_dict, values=values)
# result = sql_td_bot.sql_connect_mdwiki_new(query, return_dict=return_dict, values=values)
# ---

"""
import copy
import os
import sys
import pymysql

# ---
from pywikibot import config
from newapi import pymysql_bot
from pathlib import Path

conversions = pymysql.converters.conversions
conversions[pymysql.FIELD_TYPE.DATE] = lambda x: str(x)
# ---
Dir = str(Path(__file__).parents[0])
dir2 = Dir.replace("\\", "/").split("/pybot/")[0]
# ---
db_username = config.db_username
db_password = config.db_password
# ---
if config.db_connect_file is None:
    credentials = {"user": db_username, "password": db_password}
else:
    credentials = {"read_default_file": config.db_connect_file}
    # read default fil
    db_username = "s55992" if dir2.find("medwiki") != -1 else "s54732"
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
main_args_new = copy.deepcopy(main_args)
main_args_new["db"] = f"{db_username}__mdwiki_new"
# ---
# if "localhost" in sys.argv or dir2 == "I:/mdwiki":
if "localhost" in sys.argv or not os.getenv("HOME"):
    credentials = {"user": "root", "password": "root11"}
    main_args["host"] = "127.0.0.1"
    main_args_new["host"] = "127.0.0.1"
    main_args["db"] = f"{db_username}__mdwiki"
    main_args_new["db"] = f"{db_username}__mdwiki_new"
    print("sql_td_bot localhost")


def sql_connect_pymysql(query, return_dict=False, values=None, many=False, **kwargs):
    # ---
    results = pymysql_bot.sql_connect_pymysql(query, return_dict=return_dict, values=values, main_args=main_args, credentials=credentials, conversions=conversions, many=many, **kwargs)
    # ---
    return results


def sql_connect_mdwiki_new(query, return_dict=False, values=None, many=False, **kwargs):
    # ---
    results = pymysql_bot.sql_connect_pymysql(query, return_dict=return_dict, values=values, main_args=main_args_new, credentials=credentials, conversions=conversions, many=many, **kwargs)
    # ---
    return results
