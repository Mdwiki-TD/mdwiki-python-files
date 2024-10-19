#!/usr/bin/python3
"""
python3 core8/pwb.py db_work/days_7

"""
#
# (C) Ibrahem Qasim, 2023
#
#
from mdapi_sql import sql_for_mdwiki

# sql_for_mdwiki.mdwiki_sql(query , update = False)
# ---
qua = """
select * from pages
where target = '' and date < DATE_SUB(current_timestamp(), INTERVAL 7 DAY)
"""
# ---
pages = sql_for_mdwiki.mdwiki_sql(qua)
# ---
for n, page in enumerate(pages, start=1):
    print(page)
# ---
qua_del = """
delete from pages
where target = ''
# and DATEDIFF(CURDATE(),date) > 7
# and date < ADDDATE(CURDATE(), INTERVAL -7 DAY)
# and date < DATE_SUB(CURDATE(), INTERVAL 7 DAY)
and date < DATE_SUB(current_timestamp(), INTERVAL 7 DAY)
"""
# ---
print(qua_del)
# ---
ty = sql_for_mdwiki.mdwiki_sql(qua_del, update=True)
# ---
print(ty)
# ---
