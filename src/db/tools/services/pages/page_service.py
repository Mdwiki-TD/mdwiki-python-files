"""
SQLAlchemy-based service for managing pages and page targets.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, List

from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError

from ...models import PageRecord
from ..analytics.word_service import get_word_counts_for_title
from ..session import get_session

logger = logging.getLogger(__name__)


def list_translated(lang: str = "All", limit: int = 500, offset: int = 0) -> List[PageRecord]:
    """Return translated pages (target not empty) optionally filtered by language."""
    with get_session() as session:
        query = session.query(PageRecord).filter(PageRecord.target.isnot(None), PageRecord.target != "")
        if lang and lang.lower() != "all":
            query = query.filter(PageRecord.lang == lang)
        return query.order_by(PageRecord.id.desc()).limit(limit).offset(offset).all()


def count_translated(lang: str = "All") -> int:
    """Return total count of translated pages, optionally filtered by language."""
    with get_session() as session:
        query = session.query(func.count(PageRecord.id)).filter(PageRecord.target.isnot(None), PageRecord.target != "")
        if lang and lang.lower() != "all":
            query = query.filter(PageRecord.lang == lang)
        return int(query.scalar() or 0)


def get_by_id(page_id: int) -> PageRecord | None:
    """Return a single page row by id, or None when missing."""
    with get_session() as session:
        return session.get(PageRecord, page_id)


def get_page_by_id(page_id: int) -> PageRecord | None:
    """Return a single page row by id, or None when missing."""
    with get_session() as session:
        return session.get(PageRecord, page_id)


def list_pages() -> List[PageRecord]:
    """Return all pages."""
    with get_session() as session:
        orm_objs = session.query(PageRecord).order_by(PageRecord.id.asc()).all()
        return orm_objs


def list_pages_by_lang_cat(lang: str, cat: str) -> List[PageRecord]:
    """Return pages filtered by language and category."""
    with get_session() as session:
        return session.query(PageRecord).filter(PageRecord.lang == lang, PageRecord.cat == cat).all()


def add_page(
    sourcetitle: str,
    translate_type: str,
    cat: str,
    lang: str,
    user: str,
    target: str,
    mdwiki_revid: int | None = None,
    word: int = 0,
) -> PageRecord:
    """Add a page and return the created record."""
    if not sourcetitle:
        raise ValueError("Title is required")
    with get_session() as session:
        orm_obj = PageRecord(
            title=sourcetitle,
            word=word,
            translate_type=translate_type,
            cat=cat,
            lang=lang,
            user=user,
            pupdate=func.current_date(),
            target=target,
            mdwiki_revid=mdwiki_revid,
        )
        session.add(orm_obj)
        try:
            session.commit()
            session.refresh(orm_obj)
            return orm_obj
        except IntegrityError as e:
            logger.error(f"Failed to add page (integrity error): {e}")
            session.rollback()
            raise ValueError(f"Page with title '{sourcetitle}' already exists") from e
        except Exception as e:
            logger.error(f"Failed to add page: {e}")
            session.rollback()
            raise


def insert_page_target(
    sourcetitle: str,
    translate_type: str,
    cat: str,
    lang: str,
    user: str,
    target: str,
    mdwiki_revid: int | None = None,
    word: int = 0,
) -> bool:
    """Insert a page target record and return success status."""
    try:
        add_page(
            sourcetitle=sourcetitle,
            translate_type=translate_type,
            cat=cat,
            lang=lang,
            user=user,
            target=target,
            mdwiki_revid=mdwiki_revid,
            word=word,
        )
        return True
    except Exception as e:
        logger.error(f"Failed to insert page target: {e}")
        return False


def update_page(
    page_id: int,
    title: str,
    target: str,
    **kwargs: Any,
) -> PageRecord:
    """Update page."""
    with get_session() as session:
        orm_obj = session.get(PageRecord, page_id)
        if not orm_obj:
            raise LookupError(f"Page id {page_id} was not found")

        orm_obj.title = title
        orm_obj.target = target

        for key, value in kwargs.items():
            if hasattr(orm_obj, key):
                setattr(orm_obj, key, value)

        try:
            session.commit()
            session.refresh(orm_obj)
        except Exception:
            logger.exception("Failed to update page")
            session.rollback()
            raise
        return orm_obj


def set_page_target(
    record: PageRecord,
    target: str,
) -> bool:
    """ """
    with get_session() as session:
        record.target = target
        record.pupdate = datetime.now().strftime("%Y-%m-%d")

        try:
            session.commit()
        except Exception:
            logger.exception("Failed to update page target")
            session.rollback()
            return False

        return True


def find_page_record(
    title: str,
    lang: str,
    user: str,
) -> PageRecord | None:
    """
    Check if record exists
    """

    with get_session() as session:
        # Check existence
        orm_obj = (
            session.query(PageRecord)
            .filter(
                PageRecord.title == title,
                PageRecord.lang == lang,
                PageRecord.user == user,
            )
            .first()
        )
        return orm_obj


def add_translate_row_to_db(
    title: str,
    translate_type: str,
    cat: str,
    lang: str,
    user: str,
    target: str,
    pupdate: str,
    word: int = 0,
) -> bool:
    """Mirror of PHP add_pages_to_db + insert_to_pages.

    Replaces ``_`` with `` `` in string values, UPDATEs rows where target is
    empty, then INSERTs a new row if no matching title+lang+user exists.
    """
    translate_type = translate_type or "lead"
    cat = cat or "RTT"

    if word == 0:
        lead_words, all_words = get_word_counts_for_title(title)
        if translate_type == "all":
            word = all_words or 0
        else:
            word = lead_words or 0

    title = title.replace("_", " ")
    user = user.replace("_", " ")
    target = target.replace("_", " ")
    cat = cat.replace("_", " ")
    lang = lang.replace("_", " ")
    pupdate = pupdate.replace("_", " ")

    with get_session() as session:
        try:
            session.query(PageRecord).filter(
                PageRecord.user == user,
                PageRecord.title == title,
                PageRecord.lang == lang,
                or_(PageRecord.target == "", PageRecord.target.is_(None)),
            ).update(
                {PageRecord.target: target, PageRecord.pupdate: pupdate, "word": word},
                synchronize_session=False,
            )
        except Exception:
            logger.exception("Failed to update existing page target")
            session.rollback()
            return False

        existing = (
            session.query(PageRecord)
            .filter(PageRecord.title == title, PageRecord.lang == lang, PageRecord.user == user)
            .first()
        )

        if not existing:
            try:
                new_page = PageRecord(
                    title=title,
                    word=word,
                    translate_type=translate_type,
                    cat=cat,
                    lang=lang,
                    user=user,
                    target=target,
                    pupdate=pupdate,
                    date=func.current_date(),
                )
                session.add(new_page)
                session.commit()
            except Exception:
                logger.exception("Failed to insert new page")
                session.rollback()
                return False

        found = (
            session.query(PageRecord)
            .filter(
                PageRecord.title == title, PageRecord.lang == lang, PageRecord.user == user, PageRecord.target == target
            )
            .first()
        )
        return found is not None


__all__ = [
    "get_page_by_id",
    "set_page_target",
    "find_page_record",
    "list_pages",
    "list_pages_by_lang_cat",
    "add_page",
    "update_page",
    "insert_page_target",
    "add_translate_row_to_db",
]
