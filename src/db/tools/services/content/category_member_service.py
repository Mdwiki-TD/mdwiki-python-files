"""
SQLAlchemy-based service for managing category_members table.
"""

from __future__ import annotations

import logging
from typing import List

from sqlalchemy import text

from ...models import CategoryMemberRecord
from ..session import get_session

logger = logging.getLogger(__name__)


def get_all_category_members() -> dict[str, list[str]]:
    """Return {category: [article_id, ...]} mapping.

    Mirrors old ``sql_for_mdwiki.get_db_category_members()``.
    """
    data: dict[str, list[str]] = {}
    with get_session() as session:
        rows = session.query(CategoryMemberRecord.category, CategoryMemberRecord.article_id).all()
        for category, article_id in rows:
            data.setdefault(category, []).append(article_id)
    return data


def list_distinct_article_ids() -> list[str]:
    """Return distinct article_id values from category_members.

    Mirrors old ``select DISTINCT article_id from category_members``.
    """
    with get_session() as session:
        rows = (
            session.query(CategoryMemberRecord.article_id)
            .distinct()
            .all()
        )
        return [row.article_id for row in rows]


def count_by_category(category: str) -> int:
    """Return the number of members in *category*."""
    with get_session() as session:
        return (
            session.query(CategoryMemberRecord)
            .filter(CategoryMemberRecord.category == category)
            .count()
        )


def get_members_by_category(category: str) -> List[CategoryMemberRecord]:
    """Return all member records for *category*."""
    with get_session() as session:
        return (
            session.query(CategoryMemberRecord)
            .filter(CategoryMemberRecord.category == category)
            .all()
        )


def add_category_member(category: str, article_id: str) -> bool:
    """Insert a single category member row. Returns True on success."""
    with get_session() as session:
        try:
            existing = (
                session.query(CategoryMemberRecord)
                .filter(
                    CategoryMemberRecord.category == category,
                    CategoryMemberRecord.article_id == article_id,
                )
                .first()
            )
            if existing:
                return True
            orm_obj = CategoryMemberRecord(category=category, article_id=article_id)
            session.add(orm_obj)
            session.commit()
            return True
        except Exception:
            logger.exception("Failed to add category member %s / %s", category, article_id)
            session.rollback()
            return False


def batch_sync_category_members(data: list[dict]) -> None:
    """Insert only new category_member rows, skipping existing ones.

    Accepts a list of dicts with keys ``category`` and ``article_id``.
    Mirrors the diff-and-insert pattern from ``all_articles.py``.
    Querying the entire category_members table into memory (existing_rows) is highly inefficient and redundant because INSERT IGNORE is used. As the table grows, this will cause severe performance degradation and potential OOM errors. We can simply deduplicate the input data in memory and let INSERT IGNORE handle skipping existing rows in the database.


    """
    with get_session() as session:
        try:
            existing_rows = set(
                session.query(CategoryMemberRecord.category, CategoryMemberRecord.article_id).all()
            )
            new_rows = []
            for row in data:
                cat = row.get("category", "")
                aid = row.get("article_id", "")
                if cat and aid and (cat, aid) not in existing_rows:
                    new_rows.append({"category": cat, "article_id": aid})

            if new_rows:
                session.execute(
                    text("""
                        INSERT IGNORE INTO category_members (category, article_id)
                        VALUES (:category, :article_id)
                    """),
                    new_rows,
                )
                session.commit()
                logger.info("Inserted %s new category_member rows", len(new_rows))
            else:
                logger.info("No new category_member rows to insert")
        except Exception:
            logger.exception("Failed to sync category members")
            session.rollback()
            raise


__all__ = [
    "get_all_category_members",
    "list_distinct_article_ids",
    "count_by_category",
    "get_members_by_category",
    "add_category_member",
    "batch_sync_category_members",
]
