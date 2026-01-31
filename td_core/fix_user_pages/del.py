#!/usr/bin/python3
"""
delete from pages_users_to_main
# delete from pages_users
WHERE id IN (
    SELECT pu.id#p.target as target, pu.target as putarget, p.lang, p.user, p.title
    FROM pages_users pu, pages p
    where pu.title = p.title
    and pu.lang = p.lang
    and pu.user = p.user
    and p.target != ""
)

python3 core8/pwb.py fix_user_pages/del

"""
import logging
import sys

import tqdm
from mdapi_sql import sql_for_mdwiki

logger = logging.getLogger(__name__)

# id, new_target, new_user, new_qid, id, title, word, translate_type, cat, lang, user, target, date, pupdate, add_date, deleted, id, title, word, translate_type, cat, lang, user, target, date, pupdate, add_date, deleted
query = """
    SELECT pum.id, pum.new_target, pum.new_user
    FROM pages_users_to_main pum, pages_users pu, pages p
    where pum.id = pu.id
    and pum.new_target = p.target
    and pu.title = p.title
    and pum.new_user = p.user
    and pu.lang = p.lang
    #and pu.user = p.user
"""

result = sql_for_mdwiki.mdwiki_sql_dict(query=query)

for x in result:
    print(x)
    # ---
    query = "DELETE FROM pages_users_to_main WHERE id = %s"
    sql_for_mdwiki.mdwiki_sql(query=query, values=[x["id"]])
    # ---
    query = "DELETE FROM pages_users WHERE id = %s"
    sql_for_mdwiki.mdwiki_sql(query=query, values=[x["id"]])
    # ---
    find_it = sql_for_mdwiki.mdwiki_sql(query="SELECT * FROM pages_users WHERE id = %s", values=[x["id"]])
    # ---
    if len(find_it) > 0:
        logger.info("<<red>> not deleted")
    else:
        logger.info("<<green>> deleted.")
