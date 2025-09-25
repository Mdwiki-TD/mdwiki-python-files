#!/usr/bin/python3
"""

from mdpyget.bots.to_sql import to_sql
# data2 = [{"title": x, "importance": v} for x, v in assessments_tab[1].items()]
# to_sql(data2, table_name, columns, title_column="title")

"""
# ---
import sys
import tqdm
# from pymysql.converters import escape_string
# ---
from mdapi_sql import sql_for_mdwiki
from mdapi_sql import sql_for_mdwiki_new

new_tables = [
    "all_exists", "all_articles", "all_qids_exists", "all_articles_titles", "all_qids", "all_qids_titles"
]


def mdwiki_sql_one_table(table_name, query, **kwargs):
    # ---
    if table_name in new_tables:
        in_sql_list = sql_for_mdwiki_new.mdwiki_sql(query, **kwargs)
    else:
        in_sql_list = sql_for_mdwiki.mdwiki_sql(query, **kwargs)
    # ---
    return in_sql_list

def insert_dict(list_of_lines, table_name, columns, lento=10, title_column="title", IGNORE=False):
    # ---
    print(f"insert_dict({table_name}): list_of_lines: {len(list_of_lines)}")
    # ---
    done = 0
    # ---
    # co_line = "title, importance"
    co_line = ", ".join(columns)
    values_line = ", ".join(["%s"] * len(columns))
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
        mdwiki_sql_one_table(table_name, qua, values=values, many=True)
        # ---
        done += len(tab)
        # ---
        print(f"to_sql.py insert_dict({table_name}) {done} done, from {len(list_of_lines)} | batch: {lento}.")


def update_table(list_of_lines, table_name, columns, lento=10, title_column="title", update_columns=None):
    # ---
    print(f"update_table({table_name}): list_of_lines: {len(list_of_lines)}")
    # ---
    done = 0
    # ---
    columns2 = update_columns or [x for x in columns if x != title_column]
    # ---
    for i in tqdm.tqdm(range(0, len(list_of_lines), lento)):
        # ---
        tab = list_of_lines[i: i + lento]
        # ---
        for vav in tab:
            # ---
            values = [vav.get(x, "") for x in columns2]
            # ---
            set_line = ", ".join([f"{x} = %s" for x in columns2])
            # ---
            qua = f""" update {table_name} set {set_line} where {title_column} = %s """
            # ---
            values.append(vav[title_column])
            # ---
            mdwiki_sql_one_table(table_name, qua, values=values)
        # ---
        done += len(tab)
        # ---
        print(f"to_sql.py update_table({table_name}) {done} done, from {len(list_of_lines)} | batch: {lento}.")


def update_table_2(list_of_lines, table_name, columns_to_set=None, lento=10, columns_where=None):
    # ---
    columns_to_set = columns_to_set or []
    columns_where = columns_where or []
    # ---
    print(f"update_table_2({table_name}): list_of_lines: {len(list_of_lines)}")
    # ---
    done = 0
    # ---
    for i in tqdm.tqdm(range(0, len(list_of_lines), lento)):
        # ---
        tab = list_of_lines[i: i + lento]
        # ---
        for vav in tab:
            # ---
            values = [vav.get(x, "") for x in columns_to_set]
            # ---
            set_line = ", ".join([f"{x} = %s" for x in columns_to_set])
            # ---
            qua = f""" update {table_name} set {set_line} where """ + " and ".join([f"{x} = %s" for x in columns_where])
            # ---
            values.extend([vav[x] for x in columns_where])
            # ---
            mdwiki_sql_one_table(table_name, qua, values=values)
        # ---
        done += len(tab)
        # ---
        print(f"to_sql.py update_table_2({table_name}) {done} done, from {len(list_of_lines)} | batch: {lento}.")


def to_sql(data, table_name, columns, title_column="title", update_columns=None, IGNORE=False):
    # ---
    que = f'''select DISTINCT * from {table_name};'''
    # ---
    in_sql = {}
    # ---
    in_sql_list = mdwiki_sql_one_table(table_name, que, return_dict=True)
    # ---
    for q in in_sql_list:
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
    if "nodump" in sys.argv:
        print('"nodump" in sys.argv - no dump')
    else:
        insert_dict(new_data_insert, table_name, columns, title_column=title_column, IGNORE=IGNORE)
        update_table(new_data_update, table_name, columns, title_column=title_column, update_columns=update_columns)

def new_to_sql(data, table_name, columns, title_columns=["title"], update_columns=None, IGNORE=False):
    # ---
    que = f'''select DISTINCT * from {table_name};'''
    # ---
    in_sql = {}
    # ---
    in_sql_list = mdwiki_sql_one_table(table_name, que, return_dict=True)
    # ---
    for q in in_sql_list:
        title = ",".join([q[t] for t in title_columns])
        in_sql[title] = q
    # ---
    new_data_insert = []
    new_data_update = []
    # ---
    same = 0
    # ---
    data_to_compare = {",".join([tab[t] for t in title_columns]): tab for tab in data}
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
    if "nodump" in sys.argv:
        print('"nodump" in sys.argv - no dump')
    else:
        insert_dict(new_data_insert, table_name, columns, title_column=title_columns[0], IGNORE=IGNORE)
        # ---
        update_table_2(new_data_update, table_name, columns_to_set=update_columns, lento=100, columns_where=title_columns)
