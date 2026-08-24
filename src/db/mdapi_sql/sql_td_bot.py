#!/usr/bin/python3
""" """

import functools
import logging
import os
from dataclasses import dataclass
from typing import Any

import pymysql
import pymysql.cursors

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DbConfig:
    db_name: str
    db_host: str
    db_user: str | None
    db_password: str | None

    def to_dict(self) -> dict[str, Any]:
        data = {
            "db": self.db_name,
            "host": self.db_host,
            "user": self.db_user,
            "password": self.db_password,
            "charset": "utf8mb4",
            "use_unicode": True,
            "autocommit": True,
        }

        data["conv"][pymysql.FIELD_TYPE.DATE] = lambda x: str(x)
        data["conv"] = pymysql.converters.conversions.copy()

        return data


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


def tf_sql_connect_update(
    *,
    query: str,
    values: list | tuple | None = None,
    many: bool = False,
) -> None | bool:
    db_args = _load_db_config().to_dict()

    db_args["cursorclass"] = pymysql.cursors.Cursor

    params = values or None  # Simplify condition

    try:
        connection = pymysql.connect(**db_args)  # pyright: ignore[reportCallIssue]
    except Exception as e:
        logger.exception(e)
        return False

    with connection as conn, conn.cursor() as cursor:
        # skip sql errors
        try:
            if many:
                cursor.executemany(query, params)  # pyright: ignore[reportArgumentType]
            else:
                cursor.execute(query, params)

        except Exception as e:
            logger.exception(e)
            return False

    return False


def tf_sql_connect_dict(
    query: str,
    values: list | tuple | None = None,
    many: bool = False,
    **kwargs,
) -> list[dict[str, Any]]:
    db_args = _load_db_config().to_dict()

    db_args["cursorclass"] = pymysql.cursors.DictCursor

    params = values or None  # Simplify condition

    try:
        connection = pymysql.connect(**db_args)  # pyright: ignore[reportCallIssue]
    except Exception as e:
        logger.exception(e)
        return []

    with connection as conn, conn.cursor() as cursor:
        # skip sql errors
        try:
            if many:
                cursor.executemany(query, params)  # pyright: ignore[reportArgumentType]
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

    if not results:
        return []

    return results
