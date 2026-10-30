#!/usr/bin/python3
"""Sync rows into the all_qids_exists table (insert new rows, update changed ones)."""

import logging

import tqdm
from db.mdapi_sql.sql_td_bot import tf_sql_connect_dict

logger = logging.getLogger(__name__)

TABLE = "all_qids_exists"
COLUMNS = ["qid", "code", "target"]
KEY_COLUMNS = ["qid", "code"]


def _batches(items, size):
    """Yield successive slices of `items` with a progress bar."""
    for i in tqdm.tqdm(range(0, len(items), size)):
        yield items[i : i + size]


def _key(row):
    return tuple(row[c] for c in KEY_COLUMNS)


def insert_data(rows, columns=COLUMNS, batch_size=10) -> None:
    if not rows:
        return

    placeholders = ", ".join(["%s"] * len(columns))
    query = f"INSERT IGNORE INTO {TABLE} ({', '.join(columns)}) VALUES ({placeholders})"

    for batch in _batches(rows, batch_size):
        values = [tuple(row.get(c, "") for c in columns) for row in batch]
        tf_sql_connect_dict(query, values=values, many=True)


def update_rows(rows, batch_size=100) -> None:
    if not rows:
        return

    query = f"UPDATE {TABLE} SET target = %s WHERE qid = %s AND code = %s"

    for batch in _batches(rows, batch_size):
        values = [(row.get("target", ""), row["qid"], row["code"]) for row in batch]
        tf_sql_connect_dict(query, values=values, many=True)


def new_to_sql(data) -> None:
    if not data:
        return

    # Existing rows in the database, indexed by (qid, code)
    existing = {_key(row): row for row in tf_sql_connect_dict(f"SELECT DISTINCT {', '.join(COLUMNS)} FROM {TABLE};")}

    # Incoming rows, de-duplicated by key (the last one wins)
    incoming = {_key(row): row for row in data}

    to_insert, to_update = [], []

    for key, row in incoming.items():
        old = existing.get(key)

        if old is None:
            to_insert.append(row)
        elif any(str(old.get(c, "")) != str(row.get(c, "")) for c in COLUMNS):
            to_update.append(row)

    same = len(incoming) - len(to_insert) - len(to_update)
    logger.info(f"{same=}, {len(to_insert)=}, {len(to_update)=}")

    insert_data(to_insert)
    update_rows(to_update)
