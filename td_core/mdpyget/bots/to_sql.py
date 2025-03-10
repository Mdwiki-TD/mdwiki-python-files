#!/usr/bin/python3
"""

from mdpyget.bots.to_sql import to_sql
# data2 = [{"title": x, "importance": v} for x, v in assessments_tab[1].items()]
# to_sql(data2, table_name, columns, title_column="title")

"""
# ---
import tqdm
# from pymysql.converters import escape_string
# ---
from mdapi_sql import sql_for_mdwiki


def insert_dict(list_of_lines, table_name, columns, lento=10, title_column="title", IGNORE=False):
    # ---
    done = 0
    # ---
    # co_line = "title, importance"
    co_line = ", ".join(columns)
    values_line = ", ".join(["%s"] * len(columns))
    # ---
    # ---
    for i in tqdm.tqdm(range(0, len(list_of_lines), lento)):
        # ---
        tab = list_of_lines[i: i + lento]
        # ---
        values = []
        # ---
        for vav in tab:
            # ---
            values_k = [vav.get(x, "") for x in columns]
            # ---
            values_2 = []
            # ---
            for value in values_k:
                # ---
                # value = escape_string(value) if isinstance(value, str) else value
                # ---
                values_2.append(value)
            # ---
            values_2 = tuple(values_2)
            # ---
            values.append(values_2)
        # ---
        qua = f"""
            INSERT INTO {table_name} ({co_line})
            values ({values_line})
            """
        # ---
        if IGNORE:
            qua = f"""
                INSERT IGNORE INTO {table_name} ({co_line})
                values ({values_line})
                """
        # ---
        # print(qua)
        # print(values)
        # ---
        sql_for_mdwiki.mdwiki_sql(qua, values=values, many=True)
        # ---
        done += len(tab)
        # ---
        print(f"to_sql.py insert_dict() {done} done, from {len(list_of_lines)}.")


def update_table(list_of_lines, table_name, columns, lento=10, title_column="title"):
    # ---
    done = 0
    # ---
    if title_column in columns:
        columns.remove(title_column)
    # ---
    for i in tqdm.tqdm(range(0, len(list_of_lines), lento)):
        # ---
        tab = list_of_lines[i: i + lento]
        # ---
        for vav in tab:
            # ---
            values = [vav.get(x, "") for x in columns]
            # ---
            set_line = ", ".join([f"{x} = %s" for x in columns])
            # ---
            qua = f""" update {table_name} set {set_line} where {title_column} = %s """
            # ---
            values.append(vav[title_column])
            # ---
            sql_for_mdwiki.mdwiki_sql(qua, values=values)
        # ---
        done += len(tab)
        # ---
        print(f"to_sql.py update_table() {done} done, from {len(list_of_lines)}.")


def to_sql(data, table_name, columns, title_column="title"):
    # ---
    que = f'''select DISTINCT * from {table_name};'''
    # ---
    in_sql = {}
    # ---
    for q in sql_for_mdwiki.select_md_sql(que, return_dict=True):
        title = q[title_column]
        in_sql[title] = q
    # ---
    new_data_insert = []
    new_data_update = []
    # ---
    same = 0
    # ---
    data_to_compare = {x[title_column]: x for x in data}
    # ---
    for key, values in data_to_compare.items():
        if key in in_sql:
            are_the_same = True
            # ---
            for c in columns:
                if in_sql[key][c] != values[c]:
                    # new_data_update[key] = values
                    new_data_update.append(values)
                    are_the_same = False
                    break
            # ---
            if are_the_same:
                same += 1
        else:
            # new_data_insert[key] = values
            new_data_insert.append(values)
    # ---
    print(f"{same=}, {len(new_data_insert)=}, {len(new_data_update)=}")
    # ---
    insert_dict(new_data_insert, table_name, columns, title_column=title_column)
    # ---
    update_table(new_data_update, table_name, columns, title_column=title_column)
