#!/usr/bin/python3
"""

from fix_user_pages.fix_it_db_new import work_in_new_tabs_to_db_new

"""
import sys
# ---
from newapi import printe
from mdapi_sql import sql_for_mdwiki


def work_in_new_tabs_to_db_new(new_tabs_to_db):
    printe.output(f"len of new_tabs_to_db {len(new_tabs_to_db)}")
    # ---
    for tab in new_tabs_to_db:
        # ---
        old = tab["old"]
        new = tab["new"]
        # ---
        printe.output("work_in_new_tabs_to_db")
        printe.output(f"\t old: user: {old['user']}, target: {old['target']}")
        printe.output(f"\t new: user: {new['user']}, target: {new['target']}")
        # ---
        # print(new)
        # {'id': '3381', 'title': 'Sympathetic crashing acute pulmonary edema', 'lang': 'ar', 'user': 'Karimabenkrid', 'pupdate': '2025-03-26', 'target': 'استسقاء رئوي حاد مفاجئ ودي', 'add_date': '2025-03-26 23:43:12'}
        # ---
        sql_for_mdwiki.insert_to_pages_users_to_main(new["id"], new["target"], new["user"], new["qid"])
