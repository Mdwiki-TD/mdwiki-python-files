#!/usr/bin/python3
"""

from td_core.fix_user_pages.fix_it_db import work_in_new_tabs_to_db

"""
# ---
import logging
import sys

from db.mdapi_sql.services import sql_for_mdwiki

logger = logging.getLogger(__name__)

all_infos_data = sql_for_mdwiki.select_md_sql(
    "SELECT w_title, w_lead_words, w_all_words FROM words;",
    return_dict=True,
)
# Index by title for O(1) lookup downstream. Previously this was loaded from
# `all_articles`, which never carried the `w_lead_words` / `w_all_words`
# columns, so `data.get("w_lead_words")` always returned None and the `word`
# field on new pages was silently never populated. Pointing at `words`
# (the actual source of those columns) restores the intended behaviour.
all_infos = {x["w_title"]: x for x in all_infos_data}


def work_in_new_tabs_to_db(new_tabs_to_db) -> None:
    logger.info(f"len of new_tabs_to_db {len(new_tabs_to_db)}")
    # ---
    for tab in new_tabs_to_db:
        # ---
        old = tab["old"]
        new = tab["new"]
        # ---
        if new.get("id"):
            del new["id"]
        # ---
        logger.info("")
        logger.info(f"\t old: user: {old['user']}, target: {old['target']}")
        logger.info(f"\t new: user: {new['user']}, target: {new['target']}")
        # ---
        # logger.info(new)
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
                new["word"] = (
                    data.get("w_lead_words") if new.get("translate_type") == "lead" else data.get("w_all_words")
                )
        # ---
        sql_for_mdwiki.add_new_to_pages(new)
        # ---
        qua = "select DISTINCT * from pages where target = %s and user = %s and lang = %s"
        params = [new["target"], new["user"], new["lang"]]
        # ---
        find_it = sql_for_mdwiki.mdwiki_sql_dict(qua, values=params)
        # ---
        if find_it:
            logger.info(f"<<green>> find_it: {find_it}")
            # ---
            # del it from pages_users
            del_it = sql_for_mdwiki.mdwiki_sql("delete from pages_users where id = %s", values=[old["id"]])
            # ---
            logger.info(f"<<green>> del_it: {del_it}")
