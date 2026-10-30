#!/usr/bin/python3
""" """

import logging
import sys

import tqdm
from db.mdapi_sql.services import sql_for_mdwiki

logger = logging.getLogger(__name__)


def _insert_dict(
    list_of_lines,
    table_name: str,
    columns,
    lento: int = 10,
    ignore: bool = False,
) -> None:

    logger.info(f"insert dict({table_name}): list_of_lines: {len(list_of_lines)}")

    if not list_of_lines:
        return

    done = 0

    # co_line = "title, importance"
    co_line = ", ".join(columns)
    values_line = ", ".join(["%s"] * len(columns))

    for i in tqdm.tqdm(range(0, len(list_of_lines), lento)):
        tab = list_of_lines[i : i + lento]

        values = []

        for vav in tab:
            values_k = [vav.get(x, "") for x in columns]

            values_2 = []

            for value in values_k:
                # value = escape_string(value) if isinstance(value, str) else value

                values_2.append(value)

            values_2 = tuple(values_2)

            values.append(values_2)

        qua = f"""
            INSERT INTO {table_name} ({co_line})
            values ({values_line})
            """

        if ignore:
            qua = f"""
                INSERT IGNORE INTO {table_name} ({co_line})
                values ({values_line})
                """

        sql_for_mdwiki.mdwiki_sql_update(qua, values=values, many=True)

        done += len(tab)

        logger.info(f"to_sql.py insert dict({table_name}) {done} done, from {len(list_of_lines)} | batch: {lento}.")


def _update_table(
    list_of_lines,
    table_name: str,
    columns_to_set,
    lento: int = 10,
    title_column: str = "title",
    update_columns=None,
) -> None:

    logger.info(f"update_table({table_name}): list_of_lines: {len(list_of_lines)}")

    if not list_of_lines:
        return

    done = 0

    columns2 = update_columns or [x for x in columns_to_set if x != title_column]

    for i in tqdm.tqdm(range(0, len(list_of_lines), lento)):
        tab = list_of_lines[i : i + lento]

        for vav in tab:
            values = [vav.get(x, "") for x in columns2]

            set_line = ", ".join([f"{x} = %s" for x in columns2])

            qua = f""" update {table_name} set {set_line} where {title_column} = %s """

            values.append(vav[title_column])

            sql_for_mdwiki.mdwiki_sql_update(qua, values=values)

        done += len(tab)

        logger.info(f"to_sql.py update table({table_name}) {done} done, from {len(list_of_lines)} | batch: {lento}.")


def to_sql(
    data,
    table_name: str,
    columns,
    title_column: str = "title",
    update_columns=None,
    ignore: bool = False,
) -> None:

    que = f"""select DISTINCT * from {table_name};"""

    in_sql = {}

    in_sql_list = sql_for_mdwiki.mdwiki_sql_dict(que)

    for q in in_sql_list:
        title = q[title_column]
        in_sql[title] = q

    new_data_insert = []
    new_data_update = []

    same = 0

    data_to_compare = {x[title_column]: x for x in data}

    for key, values in data_to_compare.items():
        if key in in_sql:
            are_the_same = True

            for c in columns:
                if str(in_sql[key].get(c, "")) != str(values.get(c, "")):
                    # new_data_update[key] = values
                    new_data_update.append(values)
                    are_the_same = False
                    break

            if are_the_same:
                same += 1
        else:
            # new_data_insert[key] = values
            new_data_insert.append(values)

    logger.info(f"{same=}, {len(new_data_insert)=}, {len(new_data_update)=}")

    if "nodump" in sys.argv:
        logger.info('"nodump" in sys.argv - no dump')
    else:
        _insert_dict(
            new_data_insert,
            table_name,
            columns,
            ignore=ignore,
        )
        _update_table(
            new_data_update,
            table_name,
            columns_to_set=columns,
            title_column=title_column,
            update_columns=update_columns,
        )
