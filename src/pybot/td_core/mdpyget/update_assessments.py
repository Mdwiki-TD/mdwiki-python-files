#!/usr/bin/python3
"""
Fetch article importance ratings from English Wikipedia (WikiProject Medicine)
and store them in the `assessments` table of the mdwiki database.

USED IN mdwiki-jobs.yaml
"""

import logging
import re
from collections.abc import Iterator

import tqdm

from db.mdapi_sql.services import sql_for_mdwiki
from md_core_helps.bots.en_to_md import enwiki_to_mdwiki
from mdwiki_api.wiki_page import newapi

logger = logging.getLogger(__name__)

api_new = newapi("en", family="wikipedia")

# Importance values that carry no information and may be overwritten.
EMPTY_IMPORTANCE = {"", "na", "unknown"}

TABLE_NAME = "assessments"
VIDEO_MD_PREFIX = "Video:"
VIDEO_EN_PREFIX = "Wikipedia:VideoWiki/"
API_CHUNK_SIZE = 50
SQL_BATCH_SIZE = 100

INSERT_QUERY = f"INSERT INTO {TABLE_NAME} (title, importance) VALUES (%s, %s)"
UPDATE_QUERY = f"UPDATE {TABLE_NAME} SET importance = %s WHERE title = %s"


def is_empty_importance(value: str | None) -> bool:
    """Return True when the value is missing or a placeholder such as 'na'."""
    return (value or "").strip().lower() in EMPTY_IMPORTANCE


def batched(items: list, size: int) -> Iterator[list]:
    """Yield successive slices of items, showing a progress bar."""
    for start in tqdm.tqdm(range(0, len(items), size)):
        yield items[start : start + size]


def get_importance(page: dict, title: str) -> str:
    """Extract the importance of a page from the Medicine project, falling back to VideoWiki for video pages."""
    assessments = page.get("pageassessments", {})

    importance = assessments.get("Medicine", {}).get("importance", "")

    if is_empty_importance(importance) and title.startswith(VIDEO_EN_PREFIX):
        importance = assessments.get("Videowiki", {}).get("importance", "")

    return importance


def fetch_page_assessments(en_keys: list[str]) -> dict[str, str]:
    """Return {mdwiki title: importance} for every title that has a real importance value."""
    data: dict[str, str] = {}

    en_keys = [re.sub(rf"^{VIDEO_MD_PREFIX}", VIDEO_EN_PREFIX, x, flags=re.IGNORECASE) for x in en_keys]

    for i in range(0, len(en_keys), API_CHUNK_SIZE):
        group = en_keys[i : i + API_CHUNK_SIZE]

        logger.info(f"get_page_assessments: len of group: {len(group)}")

        for page in api_new.get_page_assessments("|".join(group)):
            title = page["title"]

            importance = get_importance(page, title)

            if is_empty_importance(importance):
                continue

            # Map the English title back to the mdwiki title.
            title = title.replace(VIDEO_EN_PREFIX, VIDEO_MD_PREFIX)
            title = enwiki_to_mdwiki.get(title, title)

            data[title] = importance

    logger.info(f"len of new assessments: {len(data)}")

    return data


def save_assessments(data: dict[str, str], from_sql: dict[str, str]) -> None:
    """Insert new titles, and update existing ones only if their stored importance is empty."""
    to_insert = [(title, importance) for title, importance in data.items() if title not in from_sql]

    to_update = [
        (importance, title)
        for title, importance in data.items()
        if title in from_sql and is_empty_importance(from_sql[title])
    ]

    logger.info(f"to insert: {len(to_insert)}, to update: {len(to_update)}")

    for query, rows in ((INSERT_QUERY, to_insert), (UPDATE_QUERY, to_update)):
        for batch in batched(rows, SQL_BATCH_SIZE):
            sql_for_mdwiki.mdwiki_sql_update(query, values=batch, many=True)


def main() -> None:
    rows = sql_for_mdwiki.mdwiki_sql_dict("SELECT DISTINCT article_id FROM category_members")
    all_titles = [x["article_id"] for x in rows]

    in_sql = sql_for_mdwiki.mdwiki_sql_dict(f"SELECT DISTINCT title, importance FROM {TABLE_NAME}")
    from_sql = {x["title"]: x["importance"] for x in in_sql}

    logger.info(f"len of all_titles: {len(all_titles)}, old assessments: {len(from_sql)}")

    data = fetch_page_assessments(all_titles)

    save_assessments(data, from_sql)


if __name__ == "__main__":
    main()
