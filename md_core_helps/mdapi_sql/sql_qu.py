#!/usr/bin/python3
"""

بوت قواعد البيانات

from mdapi_sql import sql_qu
can_use_sql_db = sql_qu.can_use_sql_db
results = sql_qu.make_sql_connect( query, db='', host='', update=False, Return=[], return_dict=False)
"""
#
# (C) Ibrahem Qasim, 2023
#
#
import os
import pymysql
import pymysql.cursors
from pywikibot import config

from newapi.except_err import exception_err
from newapi import printe

db_username = config.db_username
db_password = config.db_password
# ---
if config.db_connect_file is None:
    credentials = {"user": db_username, "password": db_password}
else:
    credentials = {"read_default_file": config.db_connect_file}
# ---
can_use_sql_db = {1: True}
# ---
dir1 = "/mnt/nfs/labstore-secondary-tools-project/"
dir2 = "/data/project/"
# ---
if not os.path.isdir(dir1) and not os.path.isdir(dir2):
    can_use_sql_db[1] = False


def sql_connect_pymysql(query, db="", host="", update=False, Return=[], return_dict=False, values=None):
    # ---
    # printe.output("start sql_connect_pymysql:")
    Typee = pymysql.cursors.DictCursor if return_dict else pymysql.cursors.Cursor
    # ---
    args2 = {
        "host": host,
        "db": db,
        "charset": "utf8mb4",
        "cursorclass": Typee,
        "use_unicode": True,
        "autocommit": True,
    }
    # ---
    params = values if values else None
    # ---
    # connect to the database server without error
    # ---
    try:
        connection = pymysql.connect(**args2, **credentials)
    except Exception as e:
        exception_err(e)
        return Return
    # ---
    with connection as conn, conn.cursor() as cursor:
        # ---
        # skip sql errors
        try:
            cursor.execute(query, params)

        except Exception as e:
            exception_err(e)
            return Return
        # ---
        results = Return
        # ---
        try:
            results = cursor.fetchall()

        except Exception as e:
            exception_err(e)
            return Return
        # ---
        # yield from cursor
        return results


def decode_value(value):
    try:
        value = value.decode("utf-8")  # Assuming UTF-8 encoding
    except BaseException:
        try:
            value = str(value)
        except BaseException:
            return ""
    return value


def resolve_bytes(rows):
    decoded_rows = []
    # ---
    for row in rows:
        decoded_row = {}
        for key, value in row.items():
            if isinstance(value, bytes):
                value = decode_value(value)
            decoded_row[key] = value
        decoded_rows.append(decoded_row)
    # ---
    return decoded_rows


def make_sql_connect(query, db="", host="", update=False, Return=[], return_dict=False, values=None, u_print=True):
    # ---
    if not query:
        printe.output("query == ''")
        return Return
    # ---
    if u_print:
        printe.output("<<yellow>> newsql::")
    # ---
    rows = sql_connect_pymysql(query, db=db, host=host, update=update, Return=Return, return_dict=return_dict, values=values)
    # ---
    if return_dict:
        rows = resolve_bytes(rows)
    # ---
    return rows
