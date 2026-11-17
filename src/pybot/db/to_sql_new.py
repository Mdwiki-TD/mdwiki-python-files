#!/usr/bin/python3
"""
Helpers for syncing a list of dict rows with a table in the mdwiki database:
rows missing from the table are inserted, rows that differ are updated.

Pass "nodump" on the command line to run everything except the writes.
"""

import logging
import sys
from collections.abc import Callable
from typing import Any

import tqdm
from db.mdapi_sql.services import sql_for_mdwiki

logger = logging.getLogger(__name__)

DEFAULT_BATCH_SIZE = 10
UPDATE_BATCH_SIZE = 100


def run_in_batches(rows: list, batch_size: int, label: str, handler: Callable[[list], None]) -> None:
    """Split rows into batches, call handler(batch) for each, and log progress."""
    total = len(rows)
    logger.info(f"{label}: {total} rows")

    done = 0
    for start in tqdm.tqdm(range(0, total, batch_size)):
        batch = rows[start : start + batch_size]
        handler(batch)

        done += len(batch)
        logger.info(f"{label}: {done} done, from {total} | batch: {batch_size}.")


def insert_dict(
    list_of_lines: list[dict],
    table_name: str,
    columns: list[str],
    lento: int = DEFAULT_BATCH_SIZE,
    ignore: bool = False,
) -> None:
    """Insert dict rows into table_name, using only the given columns."""
    if not list_of_lines:
        return

    verb = "INSERT IGNORE" if ignore else "INSERT"
    placeholders = ", ".join(["%s"] * len(columns))
    query = f"{verb} INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    def handler(batch: list[dict]) -> None:
        values = [tuple(row.get(col, "") for col in columns) for row in batch]
        sql_for_mdwiki.mdwiki_sql_update(query, values=values, many=True)

    run_in_batches(list_of_lines, lento, f"insert_dict({table_name})", handler)


def update_table(
    list_of_lines: list[dict],
    table_name: str,
    columns_to_set: list[str],
    columns_where: list[str],
    lento: int = UPDATE_BATCH_SIZE,
) -> None:
    """Update rows in table_name: set columns_to_set where columns_where match."""
    if not list_of_lines:
        return

    # The query is identical for every row, so build it once.
    set_line = ", ".join(f"{col} = %s" for col in columns_to_set)
    where_line = " AND ".join(f"{col} = %s" for col in columns_where)
    query = f"UPDATE {table_name} SET {set_line} WHERE {where_line}"

    def handler(batch: list[dict]) -> None:
        values = [
            tuple(row.get(col, "") for col in columns_to_set) + tuple(row[col] for col in columns_where)
            for row in batch
        ]
        sql_for_mdwiki.mdwiki_sql_update(query, values=values, many=True)

    run_in_batches(list_of_lines, lento, f"update_table({table_name})", handler)


def split_new_and_changed(
    data: list[dict[str, Any]],
    existing: list[dict[str, Any]],
    columns: list[str],
    title_columns: list[str],
) -> tuple[list[dict], list[dict]]:
    """Return (rows to insert, rows to update) by comparing data with the existing table rows."""

    def key_of(row: dict) -> tuple:
        return tuple(row[col] for col in title_columns)

    existing_by_key = {key_of(row): row for row in existing}

    # Later duplicates in data win.
    data_by_key = {key_of(row): row for row in data}

    to_insert = []
    to_update = []

    for key, row in data_by_key.items():
        old = existing_by_key.get(key)

        if old is None:
            to_insert.append(row)
        elif any(str(old.get(col, "")) != str(row.get(col, "")) for col in columns):
            to_update.append(row)

    same = len(data_by_key) - len(to_insert) - len(to_update)
    logger.info(f"{same=}, {len(to_insert)=}, {len(to_update)=}")

    return to_insert, to_update


def new_to_sql(
    data: list[dict[str, Any]],
    table_name: str,
    columns: list[str],
    in_sql_list: list[dict[str, Any]] | None = None,
    title_columns: list[str] | None = None,
    update_columns: list[str] | None = None,
    ignore: bool = False,
) -> None:
    """Sync data with table_name, matching rows by title_columns (default: ["title"])."""
    if not data:
        return

    title_columns = title_columns or ["title"]

    # By default every non-key column is updated.
    update_columns = update_columns or [col for col in columns if col not in title_columns]

    if in_sql_list is None:
        in_sql_list = sql_for_mdwiki.mdwiki_sql_dict(f"SELECT DISTINCT * FROM {table_name};")

    to_insert, to_update = split_new_and_changed(data, in_sql_list, columns, title_columns)

    if "nodump" in sys.argv:
        logger.info('"nodump" in sys.argv - no dump')
        return

    insert_dict(to_insert, table_name, columns, ignore=ignore)

    update_table(to_update, table_name, columns_to_set=update_columns, columns_where=title_columns)
