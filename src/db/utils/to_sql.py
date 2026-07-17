"""
Generic batch INSERT / UPDATE / upsert helpers using SQLAlchemy reflection.

Replaces the old pymysql-based version.  Reflects table metadata at runtime
so it works with any table name.
"""

from __future__ import annotations

import logging
import sys
from typing import Any, Dict, List, Optional

import tqdm
from sqlalchemy import MetaData, Table, insert, select, text, update
from sqlalchemy.dialects.mysql import insert as mysql_insert

from ..tools.services.session import SessionLocal, engine

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Table reflection cache
# ---------------------------------------------------------------------------
_metadata = MetaData()
_table_cache: Dict[str, Table] = {}


def _get_table(table_name: str) -> Table:
    """Return a reflected ``Table`` object (cached)."""
    if table_name not in _table_cache:
        _table_cache[table_name] = Table(table_name, _metadata, autoload_with=engine)
    return _table_cache[table_name]


def mdwiki_sql_one_table(
    table_name: str,
    query,
    **kwargs,
):
    """Legacy compatibility wrapper — callers still pass raw SQL + kwargs.

    Mirrors the old interface.  New code should use the dedicated helpers below.
    """
    with SessionLocal() as session:
        result = session.execute(text(query), kwargs.get("values") or {})
        if kwargs.get("return_dict"):
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]
        return result


def insert_dict(
    list_of_lines: List[dict],
    table_name: str,
    columns: List[str],
    lento: int = 10,
    title_column: str = "title",
    ignore: bool = False,
) -> None:
    """
    Batch INSERT rows into *table_name*.

    Parameters
    ----------
    list_of_lines
        List of dicts (keys = column names).
    table_name
        Target table.
    columns
        Column names to insert.
    lento
        Batch size.
    ignore
        If True, use INSERT IGNORE.
    """
    if not list_of_lines:
        return

    tbl = _get_table(table_name)
    logger.info("insert_dict(%s): %s rows", table_name, len(list_of_lines))
    done = 0

    for i in tqdm.tqdm(range(0, len(list_of_lines), lento)):
        batch = list_of_lines[i : i + lento]
        values_list = [{col: row.get(col, "") for col in columns} for row in batch]

        with SessionLocal() as session:
            try:
                if ignore:
                    stmt = mysql_insert(tbl).values(values_list).prefix_with("IGNORE")
                else:
                    stmt = insert(tbl).values(values_list)
                session.execute(stmt)
                session.commit()
            except Exception:
                session.rollback()
                raise

        done += len(batch)
        logger.info(
            "insert_dict(%s) %s done, from %s | batch: %s.",
            table_name,
            done,
            len(list_of_lines),
            lento,
        )


def update_table(
    list_of_lines: List[dict],
    table_name: str,
    columns: List[str],
    lento: int = 10,
    title_column: str = "title",
    update_columns: Optional[List[str]] = None,
) -> None:
    """
    Batch UPDATE rows by *title_column*.

    Parameters
    ----------
    list_of_lines
        List of dicts.
    table_name
        Target table.
    columns
        Full column list (used only to derive defaults).
    lento
        Batch size.
    title_column
        Column used in the WHERE clause.
    update_columns
        Columns to SET (default: all columns except *title_column*).
    """
    if not list_of_lines:
        return

    tbl = _get_table(table_name)
    cols_to_set = update_columns or [c for c in columns if c != title_column]
    logger.info("update_table(%s): %s rows", table_name, len(list_of_lines))
    done = 0

    for i in tqdm.tqdm(range(0, len(list_of_lines), lento)):
        batch = list_of_lines[i : i + lento]

        with SessionLocal() as session:
            try:
                for row in batch:
                    title_val = row.get(title_column, "")
                    if not title_val:
                        continue
                    stmt = (
                        update(tbl)
                        .where(tbl.c[title_column] == title_val)
                        .values({col: row.get(col, "") for col in cols_to_set})
                    )
                    session.execute(stmt)
                session.commit()
            except Exception:
                session.rollback()
                raise

        done += len(batch)
        logger.info(
            "update_table(%s) %s done, from %s | batch: %s.",
            table_name,
            done,
            len(list_of_lines),
            lento,
        )


def update_table_2(
    list_of_lines: List[dict],
    table_name: str,
    columns_to_set: Optional[List[str]] = None,
    lento: int = 10,
    columns_where: Optional[List[str]] = None,
) -> None:
    """
    Batch UPDATE rows using arbitrary WHERE columns.

    Parameters
    ----------
    list_of_lines
        List of dicts.
    table_name
        Target table.
    columns_to_set
        Columns to SET.
    lento
        Batch size.
    columns_where
        Columns used in the WHERE clause (ANDed together).
    """
    if not list_of_lines:
        return

    tbl = _get_table(table_name)
    columns_to_set = columns_to_set or []
    columns_where = columns_where or []
    logger.info("update_table_2(%s): %s rows", table_name, len(list_of_lines))
    done = 0

    for i in tqdm.tqdm(range(0, len(list_of_lines), lento)):
        batch = list_of_lines[i : i + lento]

        with SessionLocal() as session:
            try:
                for row in batch:
                    where_clause = [tbl.c[col] == row.get(col, "") for col in columns_where]
                    values = {col: row.get(col, "") for col in columns_to_set}
                    stmt = update(tbl).where(*where_clause).values(**values)  # type: ignore[arg-type]
                    session.execute(stmt)
                session.commit()
            except Exception:
                session.rollback()
                raise

        done += len(batch)
        logger.info(
            "update_table_2(%s) %s done, from %s | batch: %s.",
            table_name,
            done,
            len(list_of_lines),
            lento,
        )


def to_sql(
    data: List[dict],
    table_name: str,
    columns: List[str],
    title_column: str = "title",
    update_columns: Optional[List[str]] = None,
    ignore: bool = False,
) -> None:
    """
    Upsert: compare *data* with existing rows, INSERT new, UPDATE changed.

    The comparison key is *title_column* (a single column).
    """
    tbl = _get_table(table_name)

    # Fetch existing rows keyed by title_column
    with SessionLocal() as session:
        rows = session.execute(select(tbl)).all()
        in_sql: dict[str, Any] = {}
        for row in rows:
            row_dict = dict(row._mapping)
            title_val = row_dict.get(title_column, "")
            in_sql[title_val] = row_dict

    new_data_insert: List[dict] = []
    new_data_update: List[dict] = []
    same = 0

    data_by_key = {x[title_column]: x for x in data}

    for key, values in data_by_key.items():
        if key in in_sql:
            are_the_same = True
            for c in columns:
                if str(in_sql[key].get(c, "")) != str(values.get(c, "")):
                    new_data_update.append(values)
                    are_the_same = False
                    break
            if are_the_same:
                same += 1
        else:
            new_data_insert.append(values)

    logger.info("to_sql(%s): same=%s, insert=%s, update=%s", table_name, same, len(new_data_insert), len(new_data_update))

    if "nodump" in sys.argv:
        logger.info('"nodump" in sys.argv — no dump')
        return

    if new_data_insert:
        insert_dict(new_data_insert, table_name, columns, title_column=title_column, ignore=ignore)
    if new_data_update:
        update_table(new_data_update, table_name, columns, title_column=title_column, update_columns=update_columns)


def new_to_sql(
    data: List[dict],
    table_name: str,
    columns: List[str],
    in_sql_list: Optional[List[dict]] = None,
    title_columns: Optional[List[str]] = None,
    update_columns: Optional[List[str]] = None,
    ignore: bool = False,
) -> None:
    """
    Upsert with composite key support.

    The comparison key is built from *title_columns* (multiple columns joined).
    """
    if title_columns is None:
        title_columns = ["title"]
    if not data:
        return

    tbl = _get_table(table_name)

    if in_sql_list is None:
        with SessionLocal() as session:
            rows = session.execute(select(tbl)).all()
            in_sql_list = [dict(row._mapping) for row in rows]

    in_sql: dict[str, Any] = {}
    for q in in_sql_list:
        key = ",".join(str(q.get(t, "")) for t in title_columns)
        in_sql[key] = q

    new_data_insert: List[dict] = []
    new_data_update: List[dict] = []
    same = 0

    data_by_key = {",".join(str(tab.get(t, "")) for t in title_columns): tab for tab in data}

    for key, values in data_by_key.items():
        if key in in_sql:
            are_the_same = True
            for c in columns:
                if str(in_sql[key].get(c, "")) != str(values.get(c, "")):
                    new_data_update.append(values)
                    are_the_same = False
                    break
            if are_the_same:
                same += 1
        else:
            new_data_insert.append(values)

    logger.info("new_to_sql(%s): same=%s, insert=%s, update=%s", table_name, same, len(new_data_insert), len(new_data_update))

    if "nodump" in sys.argv:
        logger.info('"nodump" in sys.argv — no dump')
        return

    if new_data_insert:
        insert_dict(new_data_insert, table_name, columns, title_column=title_columns[0], ignore=ignore)
    if new_data_update:
        update_table_2(new_data_update, table_name, columns_to_set=update_columns, lento=100, columns_where=title_columns)
