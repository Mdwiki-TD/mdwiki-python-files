#!/usr/bin/python3
"""

from td_core.fix_user_pages.fix_it_db_new import work_in_new_tabs_to_db_new

"""
# ---
import logging

from db.tools.services.session import get_session
from sqlalchemy import text

logger = logging.getLogger(__name__)


def work_in_new_tabs_to_db_new(new_tabs_to_db) -> None:
    logger.info(f"len of new_tabs_to_db {len(new_tabs_to_db)}")
    # ---
    for tab in new_tabs_to_db:
        # ---
        old = tab["old"]
        new = tab["new"]
        # ---
        logger.info("work_in_new_tabs_to_db")
        logger.info(f"\t old: user: {old['user']}, target: {old['target']}")
        logger.info(f"\t new: user: {new['user']}, target: {new['target']}")
        # ---
        # logger.info(new)
        # {'id': '3381', 'title': 'Sympathetic crashing acute pulmonary edema', 'lang': 'ar', 'user': 'Karimabenkrid', 'pupdate': '2025-03-26', 'target': 'استسقاء رئوي حاد مفاجئ ودي', 'add_date': '2025-03-26 23:43:12'}
        # ---
        with get_session() as session:
            session.execute(
                text("INSERT INTO pages_users_to_main (id, new_target, new_user, new_qid) VALUES (:id, :target, :user, :qid)"),
                {"id": new["id"], "target": new["target"], "user": new["user"], "qid": new["qid"]},
            )
            session.commit()
