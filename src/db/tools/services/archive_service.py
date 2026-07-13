import logging

from sqlalchemy import select

from src.db.tools.models.archive import Archive
from src.db.tools.services.session import get_session

logger = logging.getLogger(__name__)

SKIP_ARCHIVE_IS = [
    "archive.is",
    "archive.ph",
    "archive.fo",
    "archive.li",
    "archive.md",
    "archive.vn",
    "archive.today",
]


def get_links(url: str) -> list[Archive]:
    with get_session() as session:
        stmt = select(Archive).where(Archive.url == url)
        results = session.execute(stmt).scalars().all()
        # Filter out archive.is urls
        return [r for r in results if not any(sit in r.archiveurl.lower() for sit in SKIP_ARCHIVE_IS)]


def insert_one(url: str, archiveurl: str) -> None:
    with get_session() as session:
        # Check if exists
        stmt = select(Archive).where(Archive.archiveurl == archiveurl)
        existing = session.execute(stmt).scalar_one_or_none()
        if not existing:
            new_archive = Archive(url=url, archiveurl=archiveurl)
            session.add(new_archive)

__all__ = [
    "get_links",
    "insert_one",
]
