#!/usr/bin/python3
""" """

import functools
import logging
import os
from dataclasses import dataclass

import pymysql
import pymysql.cursors

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DbConfig:
    db_name: str
    db_host: str
    db_user: str | None
    db_password: str | None

    def to_dict(self) -> dict:
        return {
            "db": self.db_name,
            "host": self.db_host,
            "user": self.db_user,
            "password": self.db_password,
            "charset": "utf8mb4",
            "use_unicode": True,
            "autocommit": True,
        }


@functools.lru_cache(maxsize=1)
def _load_db_config() -> DbConfig:
    db_user: str = os.getenv("TOOL_TOOLSDB_USER") or "root"
    db_password: str = os.getenv("TOOL_TOOLSDB_PASSWORD") or "root11"

    db_name: str = os.getenv("TOOL_TOOLSDB_DBNAME") or f"{db_user}__mdwiki"
    db_host: str = os.getenv("TOOL_TOOLSDB_HOST") or "127.0.0.1"

    return DbConfig(
        db_name=db_name,
        db_host=db_host,
        db_user=db_user,
        db_password=db_password,
    )


def wiki_sql_connect(
    query,
    values=None,
    db_args: dict = None,
    many: bool = False,
):
    params = values or None  # Simplify condition

    try:
        connection = pymysql.connect(**db_args)
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
            logger.exception("Exception during fetchall", exc_info=True)
            return []

    return results


def toolforge_tools_sql_connect(
    query,
    return_dict: bool = False,
    values=None,
    many: bool = False,
    **kwargs,
):

    db_args = _load_db_config().to_dict()

    db_args["cursorclass"] = pymysql.cursors.DictCursor if return_dict else pymysql.cursors.Cursor
    db_args["conv"] = pymysql.converters.conversions.copy()
    db_args["conv"][pymysql.FIELD_TYPE.DATE] = lambda x: str(x)

    results = wiki_sql_connect(
        query,
        values=values,
        db_args=db_args,
        many=many,
    )

    return results
