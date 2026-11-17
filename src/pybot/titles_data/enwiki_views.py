#!/usr/bin/python3
"""
Fetch article page views from English Wikipedia and store them
in the `enwiki_pageviews` table of the mdwiki database.

python3 c9/pwb.py titles_data/enwiki_views from_cats newpages nodump
python3 c9/pwb.py titles_data/enwiki_views newpages nodump
python3 c9/pwb.py titles_data/enwiki_views newpages nowork

USED IN mdwiki-jobs.yaml
"""

import logging
import re
from typing import Any

from db.mdapi_sql.services import sql_for_mdwiki
from db.to_sql_new import insert_dict, split_new_and_changed, update_table
from md_core_helps.apis.mw_views import PageviewsClient
from md_core_helps.bots.en_to_md import enwiki_to_mdwiki

logger = logging.getLogger(__name__)

TABLE_NAME = "enwiki_pageviews"
VIDEO_MD_PREFIX = "Video:"
VIDEO_EN_PREFIX = "Wikipedia:VideoWiki/"


def new_to_sql(
    data: list[dict[str, Any]],
    table_name: str,
    columns: list[str],
    in_sql_list: list[dict[str, Any]] | None = None,
    title_columns: list[str] | None = None,
    update_columns: list[str] | None = None,
    ignore: bool = False,
) -> None:
    """Sync data with table_name, matching rows by title_columns (default: ["title"])."""
    if not data:
        return

    title_columns = title_columns or ["title"]

    # By default every non-key column is updated.
    update_columns = update_columns or [col for col in columns if col not in title_columns]

    if in_sql_list is None:
        in_sql_list = sql_for_mdwiki.mdwiki_sql_dict(f"SELECT DISTINCT * FROM {table_name};")

    to_insert, to_update = split_new_and_changed(data, in_sql_list, columns, title_columns)

    insert_dict(
        to_insert,
        table_name,
        columns,
        ignore=ignore,
    )

    update_table(
        to_update,
        table_name,
        columns_to_set=update_columns,
        columns_where=title_columns,
    )


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
    logger.info(f"<<purple>> len of enviews: {len(enviews)}, with views: {len(data)}, no views: {no_views}")

    return data


def save_to_sql(data: dict[str, int], from_sql) -> None:
    """Insert new titles and update titles whose view count changed."""
    rows = [{"title": title, "en_views": views} for title, views in data.items()]

    new_to_sql(
        data=rows,
        table_name=TABLE_NAME,
        columns=["title", "en_views"],
        title_columns=["title"],
    )


def main() -> None:
    rows = sql_for_mdwiki.mdwiki_sql_dict("SELECT DISTINCT article_id FROM category_members")
    all_titles = [x["article_id"] for x in rows]

    in_sql = sql_for_mdwiki.mdwiki_sql_dict("select DISTINCT title, en_views from enwiki_pageviews")
    from_sql = {x["title"]: x["en_views"] for x in in_sql}

    logger.info(f"len of all_titles: {len(all_titles)}, old en_views: {len(from_sql)}")

    data = fetch_pages_views(all_titles)

    save_to_sql(data, from_sql)


if __name__ == "__main__":
    main()
