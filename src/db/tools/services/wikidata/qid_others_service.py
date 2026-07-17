"""
SQLAlchemy-based service for managing qids_others table.
"""

from __future__ import annotations

import logging
from typing import List

from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased

from ...models import QidOthersRecord
from ..session import get_session

logger = logging.getLogger(__name__)


def add_qid_other(title: str, qid: str) -> QidOthersRecord:
    """Add or update a QID for a title."""
    with get_session() as session:
        orm_obj = session.query(QidOthersRecord).filter(QidOthersRecord.title == title).first()
        if orm_obj:
            orm_obj.qid = qid
        else:
            orm_obj = QidOthersRecord(title=title, qid=qid)

        orm_obj.validate()

        try:
            session.add(orm_obj)
            session.commit()
            session.refresh(orm_obj)
        except Exception:
            session.rollback()
            raise
        return orm_obj


def update_qid_other(qid_id: int, title: str, qid: str) -> QidOthersRecord:
    """Update a QID record."""
    with get_session() as session:
        orm_obj = session.get(QidOthersRecord, qid_id)
        if not orm_obj:
            raise ValueError(f"QID record with ID {qid_id} not found")

        orm_obj.title = title
        orm_obj.qid = qid

        orm_obj.validate()

        try:
            session.commit()
            session.refresh(orm_obj)
        except Exception:
            session.rollback()
            raise
        return orm_obj


def get_page_qid_other(title: str) -> QidOthersRecord | None:
    """Get the QID for a page title."""
    with get_session() as session:
        orm_obj = session.query(QidOthersRecord).filter(QidOthersRecord.title == title).first()
        if not orm_obj:
            logger.warning(f"QID for title {title} not found")
            return None
        return orm_obj


def list_records(dis: str = "all") -> List[QidOthersRecord]:
    """Return qids_others records, optionally filtered by ``dis``.

    - ``"all"``: every row.
    - ``"empty"``: rows where qid is NULL or empty string.
    - ``"duplicate"``: rows that share a title or qid with another row.
    """
    with get_session() as session:
        base = session.query(QidOthersRecord)
        if dis == "empty":
            rows = (
                base.filter(or_(QidOthersRecord.qid.is_(None), QidOthersRecord.qid == ""))
                .order_by(QidOthersRecord.id.asc())
                .all()
            )
            return rows
        if dis == "duplicate":
            other = aliased(QidOthersRecord)
            rows = (
                base.join(
                    other,
                    and_(
                        QidOthersRecord.id != other.id,
                        or_(
                            QidOthersRecord.qid == other.qid,
                            QidOthersRecord.title == other.title,
                        ),
                    ),
                )
                .order_by(QidOthersRecord.id.asc())
                .distinct()
                .all()
            )
            return rows
        # default: all
        return base.order_by(QidOthersRecord.id.asc()).all()


def get_by_qid(qid: str) -> QidOthersRecord | None:
    """Get the first qids_others record matching the given qid string."""
    if not qid:
        return None
    with get_session() as session:
        return session.query(QidOthersRecord).filter(QidOthersRecord.qid == qid).first()


def get_by_id(qid_id: int) -> QidOthersRecord | None:
    """Get a QID record by its primary key ID."""
    with get_session() as session:
        return session.get(QidOthersRecord, qid_id)


def get_by_title(title: str) -> QidOthersRecord | None:
    """Get the qids_others record matching the given title."""
    if not title:
        return None
    with get_session() as session:
        return session.query(QidOthersRecord).filter(QidOthersRecord.title == title).first()


def insert(title: str, qid: str) -> bool:
    """Insert a new qids_others row, or fill a missing qid for an existing title."""
    title = (title or "").strip()
    qid = (qid or "").strip()
    if not title or not qid:
        return False
    with get_session() as session:
        try:
            existing = session.query(QidOthersRecord).filter(QidOthersRecord.title == title).first()
            if existing:
                if not existing.qid:
                    existing.qid = qid
                    session.commit()
                return True

            orm_obj = QidOthersRecord(title=title, qid=qid)
            session.add(orm_obj)
            session.commit()
            return True
        except Exception:
            logger.exception("Failed to insert qids_others title=%r qid=%r", title, qid)
            session.rollback()
            return False


def update(qid_id: int, title: str, qid: str) -> bool:
    """Update an existing qids_others row by primary key."""
    title = (title or "").strip()
    qid = (qid or "").strip()

    if not qid_id or not title or not qid:
        return False

    orm_obj = None

    with get_session() as session:
        try:
            orm_obj = session.get(QidOthersRecord, qid_id)
        except Exception:
            logger.exception("Failed to update qid id=%r", qid_id)
            return False

        if not orm_obj:
            return False

        orm_obj.title = title
        orm_obj.qid = qid

        try:
            orm_obj.validate()
        except Exception:
            logger.exception("Failed to validate")
            session.rollback()
            return False

        try:
            session.commit()
            return True
        except Exception:
            logger.exception("Failed to update qids_others id=%r", qid_id)
            session.rollback()
            return False


def list_qid_records() -> List[QidOthersRecord]:
    """Return all QID records (legacy alias kept for compatibility)."""
    with get_session() as session:
        return session.query(QidOthersRecord).order_by(QidOthersRecord.id.asc()).all()


def get_title_to_qid() -> dict[str, str]:
    """Retrieve title to QID mapping from database."""
    qids = list_qid_records()
    return {record.title: record.qid or "" for record in qids}


def update_qid_by_value(old_qid: str, new_qid: str) -> None:
    """Update all rows matching *old_qid* to *new_qid*."""
    with get_session() as session:
        rows = session.query(QidOthersRecord).filter(QidOthersRecord.qid == old_qid).all()
        for row in rows:
            row.qid = new_qid
            row.validate()
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise


def update_qid_by_title(title: str, qid: str) -> None:
    """Update the qid for the row matching *title*."""
    with get_session() as session:
        orm_obj = session.query(QidOthersRecord).filter(QidOthersRecord.title == title).first()
        if orm_obj:
            orm_obj.qid = qid
            orm_obj.validate()
            try:
                session.commit()
            except Exception:
                session.rollback()
                raise


def delete_by_title(title: str, pr: str = "") -> None:
    """Delete the qids_others row matching *title*."""
    if pr:
        logger.info("%s (qids_others) title:%s", pr, title)
    with get_session() as session:
        orm_obj = session.query(QidOthersRecord).filter(QidOthersRecord.title == title).first()
        if orm_obj:
            try:
                session.delete(orm_obj)
                session.commit()
            except Exception:
                session.rollback()
                raise


def update_title_by_qid(new_title: str, qid: str) -> None:
    """Update the title for all rows matching *qid*."""
    with get_session() as session:
        rows = session.query(QidOthersRecord).filter(QidOthersRecord.qid == qid).all()
        for row in rows:
            row.title = new_title
            row.validate()
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise


def update_title_conditionally(old_title: str, new_title: str, qid: str, no_do: bool = False) -> None:
    """Update title where qid matches and old_title matches."""
    if no_do:
        logger.info("UPDATE qids_others set title = %s where qid = %s and title = %s", new_title, qid, old_title)
        return
    with get_session() as session:
        rows = (
            session.query(QidOthersRecord)
            .filter(QidOthersRecord.qid == qid, QidOthersRecord.title == old_title)
            .all()
        )
        for row in rows:
            row.title = new_title
            row.validate()
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise


def batch_upsert_qids(tab0: dict[str, str], add_empty_qid: bool = False) -> None:
    """Batch upsert titles → qids.

    Mirrors old ``sql_qids_others.add_titles_to_qids``:
    - Filters out empty titles / empty qids (unless *add_empty_qid*)
    - Adds missing titles
    - Updates titles that exist but have different qid
    """
    if not tab0:
        logger.info("tab0 empty..")
        return

    ids_in_db = get_title_to_qid()

    tab = {t: q for t, q in tab0.items() if t.strip() and (q.strip() or add_empty_qid)}

    logger.info("len of tab: %s, tab0: %s", len(tab), len(tab0))

    same = {x: qid for x, qid in tab.items() if qid == ids_in_db.get(x)}
    not_in = {x: qid for x, qid in tab.items() if x not in ids_in_db}

    logger.info("len of ids_in_db: %s", len(ids_in_db))
    logger.info("len of same qids: %s", len(same))
    logger.info("len of not_in: %s", len(not_in))

    for title, new_qid in not_in.items():
        add_qid_other(title, new_qid)

    rest_qids = {x: qid for x, qid in tab.items() if x not in same and x not in not_in}
    logger.info("len of rest_qids: %s", len(rest_qids))

    rest_qids = {x: qid for x, qid in rest_qids.items() if qid}
    logger.info("len of rest_qids after remove empty qids: %s", len(rest_qids))

    if not rest_qids:
        return

    for title, new_qid in rest_qids.items():
        if not ids_in_db.get(title):
            update_qid_by_title(title, new_qid)

    has_diff_qid_in_db = {x: qid for x, qid in rest_qids.items() if ids_in_db.get(x)}
    logger.info("len of last_qids after remove titles in db: %s", len(has_diff_qid_in_db))

    for t, q in has_diff_qid_in_db.items():
        qid_in = ids_in_db.get(t)
        logger.info("skip... update_qid_by_title(%s) %s, %s", t, qid_in, q)


__all__ = [
    "add_qid_other",
    "update_qid_other",
    "get_page_qid_other",
    "list_records",
    "list_qid_records",
    "get_title_to_qid",
    "get_by_qid",
    "get_by_title",
    "insert",
    "update",
    "get_by_id",
    "update_qid_by_value",
    "update_qid_by_title",
    "delete_by_title",
    "update_title_by_qid",
    "update_title_conditionally",
    "batch_upsert_qids",
]
