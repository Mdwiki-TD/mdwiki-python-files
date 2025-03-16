#!/usr/bin/python3
"""

python3 core8/pwb.py db_work/days_7

"""
from mdapi_sql import sql_for_mdwiki

# sql_for_mdwiki.mdwiki_sql(query , update = False)
# ---
queries = {
    "pages": "where date < DATE_SUB(current_timestamp(), INTERVAL 7 DAY) and (target = '' OR target IS NULL)",
    "in_process": "where add_date < DATE_SUB(current_timestamp(), INTERVAL 7 DAY) ",
}
# ---
for name, qua in queries.items():
    print(f"--- {name} ---")
    # ---
    qua_select = f"select * from {name} {qua}"
    # ---
    pages = sql_for_mdwiki.mdwiki_sql_dict(qua_select)
    # ---
    for n, page in enumerate(pages, start=1):
        print(name, n, page)
    # ---
    qua_del = f"delete from {name} {qua}"
    # ---
    print(qua_del)
    # ---
    ty = sql_for_mdwiki.mdwiki_sql(qua_del, update=True)
    # ---
    print(ty)
