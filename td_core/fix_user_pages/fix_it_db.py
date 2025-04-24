#!/usr/bin/python3
"""

from fix_user_pages.fix_it_db import work_in_new_tabs_to_db

"""
import sys
# ---
from newapi import printe
from mdapi_sql import sql_for_mdwiki

all_infos = sql_for_mdwiki.get_all_from_table(table_name="titles_infos")
all_infos = {x["title"]: x for x in all_infos}


def work_in_new_tabs_to_db(new_tabs_to_db):
    printe.output(f"len of new_tabs_to_db {len(new_tabs_to_db)}")
    # ---
    for tab in new_tabs_to_db:
        # ---
        old = tab["old"]
        new = tab["new"]
        # ---
        if new.get("id"):
            del new['id']
        # ---
        printe.output("work_in_new_tabs_to_db")
        printe.output(f"\t old: user: {old['user']}, target: {old['target']}")
        printe.output(f"\t new: user: {new['user']}, target: {new['target']}")
        # ---
        # print(new)
        # {'id': '3381', 'title': 'Sympathetic crashing acute pulmonary edema', 'lang': 'ar', 'user': 'Karimabenkrid', 'pupdate': '2025-03-26', 'target': 'استسقاء رئوي حاد مفاجئ ودي', 'add_date': '2025-03-26 23:43:12'}
        # ---
        if "test" in sys.argv:
            continue
        # ---
        new["translate_type"] = new.get("translate_type") or "lead"
        # ---
        if not new.get("word") and new.get("title"):
            data = all_infos.get(new["title"])
            if data:
                new["word"] = data.get("w_lead_words") if new.get("translate_type") == "lead" else data.get("w_all_words")
        # ---
        sql_for_mdwiki.add_new_to_pages(new)
        # ---
        qua = "select DISTINCT * from pages where target = %s and user = %s and lang = %s"
        params = [new["target"], new["user"], new["lang"]]
        # ---
        find_it = sql_for_mdwiki.mdwiki_sql_dict(qua, values=params)
        # ---
        if find_it:
            printe.output(f"<<green>> find_it: {find_it}")
            # ---
            # del it from pages_users
            del_it = sql_for_mdwiki.mdwiki_sql("delete from pages_users where id = %s", values=[old['id']])
            # ---
            printe.output(f"<<green>> del_it: {del_it}")
