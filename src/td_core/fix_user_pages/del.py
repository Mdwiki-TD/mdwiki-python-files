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

python3 core8/pwb.py td_core/fix_user_pages/del

"""
import logging

from db.tools.services.session import get_session
from sqlalchemy import text

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

with get_session() as session:
    rows = session.execute(text(query)).fetchall()
    result = [dict(row._mapping) for row in rows]

    for x in result:
        logger.info(x)
        session.execute(text("DELETE FROM pages_users_to_main WHERE id = :id"), {"id": x["id"]})
        session.execute(text("DELETE FROM pages_users WHERE id = :id"), {"id": x["id"]})
    session.commit()

    # Verify deletions
    for x in result:
        rows2 = session.execute(text("SELECT * FROM pages_users WHERE id = :id"), {"id": x["id"]}).fetchall()
        if rows2:
            logger.info("<<red>> not deleted")
        else:
            logger.info("<<green>> deleted.")
