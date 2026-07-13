#!/usr/bin/python3
"""

python3 core8/pwb.py td_core/db_work/days_7

"""
import logging

from db.tools.services.session import get_session
from sqlalchemy import text

logger = logging.getLogger(__name__)


# sql_for_mdwiki.mdwiki_sql(query , update = False)
# ---
queries = {
    "pages": "where date < DATE_SUB(current_timestamp(), INTERVAL 7 DAY) and (target = '' OR target IS NULL)",
    "in_process": "where add_date < DATE_SUB(current_timestamp(), INTERVAL 7 DAY) ",
}
# ---
for name, qua in queries.items():
    logger.info(f"--- {name} ---")
    # ---
    qua_select = f"select * from {name} {qua}"
    # ---
    with get_session() as session:
        pages = [dict(row._mapping) for row in session.execute(text(qua_select))]
    # ---
    for n, page in enumerate(pages, start=1):
        print(name, n, page)
    # ---
    qua_del = f"delete from {name} {qua}"
    # ---
    logger.info(qua_del)
    # ---
    with get_session() as session:
        ty = session.execute(text(qua_del))
        session.commit()
    # ---
    logger.info(ty)
