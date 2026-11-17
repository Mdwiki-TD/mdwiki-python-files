#!/usr/bin/python3
"""
Fetch article page views from English Wikipedia and store them
in the `enwiki_pageviews` table of the mdwiki database.

USED IN mdwiki-jobs.yaml
"""

import logging
import re
from collections.abc import Iterator
from typing import Any

import tqdm
from db.mdapi_sql.services import sql_for_mdwiki
from md_core_helps.apis.mw_views import PageviewsClient
from md_core_helps.bots.en_to_md import enwiki_to_mdwiki

logger = logging.getLogger(__name__)

TABLE_NAME = "enwiki_pageviews"
VIDEO_MD_PREFIX = "Video:"
VIDEO_EN_PREFIX = "Wikipedia:VideoWiki/"
SQL_BATCH_SIZE = 100

INSERT_QUERY = f"INSERT INTO {TABLE_NAME} (title, en_views) VALUES (%s, %s)"
UPDATE_QUERY = f"UPDATE {TABLE_NAME} SET en_views = %s WHERE title = %s"


def batched(items: list, size: int) -> Iterator[list]:
    """Yield successive slices of items, showing a progress bar."""
    for start in tqdm.tqdm(range(0, len(items), size)):
        yield items[start : start + size]


def fetch_pages_views(en_keys: list[str]) -> dict[str, int]:
    """Return {mdwiki title: total views} for every title that has at least one view."""
    en_keys = [re.sub(rf"^{VIDEO_MD_PREFIX}", VIDEO_EN_PREFIX, x, flags=re.IGNORECASE) for x in en_keys]

    # Shape: {'Yemen': {'all': 187379, '2025': 187379}, ...}
    enviews = PageviewsClient().article_views_new("en.wikipedia", en_keys)

    data: dict[str, int] = {}

    for title, view in enviews.items():
        total = int(view.get("all") or 0)

        if not total:
            continue

        # Map the English title back to the mdwiki title.
        title = title.replace(VIDEO_EN_PREFIX, VIDEO_MD_PREFIX)
        title = enwiki_to_mdwiki.get(title) or title

        data[title] = total

    no_views = len(enviews) - len(data)
    logger.info(f"len of enviews: {len(enviews)}, with views: {len(data)}, no views: {no_views}")

    return data


def save_to_sql(data: dict[str, int], from_sql: dict[str, Any]) -> None:
    """Insert new titles and update titles whose view count changed."""
    to_insert = [(title, views) for title, views in data.items() if title not in from_sql]

    to_update = [
        (views, title) for title, views in data.items() if title in from_sql and str(from_sql[title]) != str(views)
    ]

    same = len(data) - len(to_insert) - len(to_update)
    logger.info(f"{same=}, {len(to_insert)=}, {len(to_update)=}")

    for query, rows in ((INSERT_QUERY, to_insert), (UPDATE_QUERY, to_update)):
        for batch in batched(rows, SQL_BATCH_SIZE):
            sql_for_mdwiki.mdwiki_sql_update(query, values=batch, many=True)


def main() -> None:
    rows = sql_for_mdwiki.mdwiki_sql_dict("SELECT DISTINCT article_id FROM category_members")
    all_titles = [x["article_id"] for x in rows]

    in_sql = sql_for_mdwiki.mdwiki_sql_dict(f"SELECT DISTINCT title, en_views FROM {TABLE_NAME}")
    from_sql = {x["title"]: x["en_views"] for x in in_sql}

    logger.info(f"len of all_titles: {len(all_titles)}, old en_views: {len(from_sql)}")

    data = fetch_pages_views(all_titles)

    save_to_sql(data, from_sql)


if __name__ == "__main__":
    main()
