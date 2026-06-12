#!/usr/bin/python3
"""

بوت قواعد البيانات

from md_core_helps.mdapi_sql import sql_qu
can_use_sql_db = sql_qu.can_use_sql_db
results = sql_qu.make_sql_connect( query, db='', host='', update=False, _return=[], return_dict=False)
"""
import functools
import logging
import os
from dataclasses import dataclass

import pymysql
import pymysql.cursors

logger = logging.getLogger(__name__)

can_use_sql_db = {1: os.getenv("APP_ENV", "").lower() == "production"}


@dataclass(frozen=True)
class WikiDbConfig:
    db_user: str | None
    db_password: str | None

    def to_dict(self) -> dict:
        return {
            "user": self.db_user,
            "password": self.db_password,
            "charset": "utf8mb4",
            "use_unicode": True,
            "autocommit": True,
        }


@functools.lru_cache(maxsize=1)
def _load_db_config() -> WikiDbConfig:
    db_user: str = os.getenv("TOOL_TOOLSDB_USER")
    db_password: str = os.getenv("TOOL_TOOLSDB_PASSWORD")

    return WikiDbConfig(
        db_user=db_user,
        db_password=db_password,
    )


def wiki_sql_connect(
    query,
    db: str="",
    host: str="",
    update: bool=False,
    _return=None,
    return_dict: bool=False,
    values=None,
):
    # ---
    _return = _return or []
    # ---
    params = values if values else None

    db_args = _load_db_config().to_dict()

    db_args["cursorclass"] = pymysql.cursors.DictCursor if return_dict else pymysql.cursors.Cursor
    db_args["conv"] = pymysql.converters.conversions.copy()
    db_args["conv"][pymysql.FIELD_TYPE.DATE] = lambda x: str(x)
    # ---
    db_args["host"] = host
    db_args["db"] = db
    # ---
    try:
        connection = pymysql.connect(**db_args)
    except Exception as e:
        logger.warning(e)
        return _return
    # ---
    with connection as conn, conn.cursor() as cursor:
        # ---
        # skip sql errors
        try:
            cursor.execute(query, params)

        except Exception as e:
            logger.warning(e)
            return _return
        # ---
        results = _return
        # ---
        try:
            results = cursor.fetchall()

        except Exception as e:
            logger.warning(e)
            return _return
        # ---
        # yield from cursor
        return results


def _decode_value(value):
    try:
        value = value.decode("utf-8")  # Assuming UTF-8 encoding
    except BaseException:
        try:
            value = str(value)
        except BaseException:
            return ""
    return value


def _resolve_bytes(rows):
    decoded_rows = []
    # ---
    for row in rows:
        decoded_row = {}
        for key, value in row.items():
            if isinstance(value, bytes):
                value = _decode_value(value)
            decoded_row[key] = value
        decoded_rows.append(decoded_row)
    # ---
    return decoded_rows


def make_sql_connect(
    query,
    db: str="",
    host: str="",
    update: bool=False,
    _return=None,
    return_dict: bool=False,
    values=None,
    u_print: bool=True,
):
    # ---
    _return = _return or []
    # ---
    if not query:
        logger.info("query == ''")
        return _return
    # ---
    if u_print:
        logger.info("<<yellow>> newsql::")
    # ---
    rows = wiki_sql_connect(
        query,
        db=db,
        host=host,
        update=update,
        _return=_return,
        return_dict=return_dict,
        values=values,
    )
    # ---
    if return_dict:
        rows = _resolve_bytes(rows)
    # ---
    return rows
