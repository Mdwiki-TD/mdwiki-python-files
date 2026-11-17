#!/usr/bin/python3
"""
Fetch yearly page views of the translated pages in every language edition
and store them in the `views_new` table of the mdwiki database.

USED IN mdwiki-jobs.yaml
"""

import logging
import re
from collections import defaultdict
from collections.abc import Iterator
from typing import Any

import tqdm

from db.mdapi_sql.services import sql_for_mdwiki
from md_core_helps.apis.mw_views import PageviewsClient

logger = logging.getLogger(__name__)

DEFAULT_START = "20210401"
END_DATE = "20300101"
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

INSERT_BATCH_SIZE = 1000
UPDATE_BATCH_SIZE = 100

INSERT_QUERY = "INSERT IGNORE INTO views_new (target, lang, year, views) VALUES (%s, %s, %s, %s)"
UPDATE_QUERY = "UPDATE views_new SET views = %s WHERE target = %s AND lang = %s AND year = %s"


def batched(items: list, size: int) -> Iterator[list]:
    """Yield successive slices of items, showing a progress bar."""
    for start in tqdm.tqdm(range(0, len(items), size)):
        yield items[start : start + size]


def get_targets() -> dict[str, dict[str, str]]:
    """Return {lang: {target title: publish date}} for every translated page."""
    rows = sql_for_mdwiki.mdwiki_sql_dict('SELECT DISTINCT lang, target, pupdate FROM pages WHERE target != ""')

    lang_to_targets: dict[str, dict[str, str]] = defaultdict(dict)

    for row in rows:
        lang_to_targets[row["lang"].lower()][row["target"]] = row["pupdate"]

    logger.info(f"find {len(rows)} to work. ")

    return lang_to_targets


def get_views_sql() -> dict[str, dict[str, dict[str, int]]]:
    """Return the stored views as {lang: {target: {year: views}}}."""
    rows = sql_for_mdwiki.mdwiki_sql_dict("SELECT DISTINCT target, lang, year, views FROM views_new")

    already_in_sql: dict[str, dict[str, dict[str, int]]] = defaultdict(lambda: defaultdict(dict))

    for row in rows:
        already_in_sql[row["lang"].lower()][row["target"]][str(row["year"])] = row["views"]

    return already_in_sql


def fetch_views(
    view_bot: PageviewsClient,
    lang: str,
    targets: dict[str, str],
) -> dict[str, dict[str, int]]:
    """Fetch daily views per target, starting from each page's publish date."""
    titles_by_date: dict[str, list[str]] = defaultdict(list)

    for target, pupdate in targets.items():
        titles_by_date[str(pupdate)].append(target)

    views: dict[str, dict[str, int]] = {}

    for pupdate, titles in titles_by_date.items():
        start = pupdate.replace("-", "") if DATE_RE.fullmatch(pupdate) else DEFAULT_START

        logger.info("---")
        logger.info(f"get pageviews for {len(titles)} pages, date_start:{start}")

        if len(titles) < 5:
            logger.info(", ".join(titles))

        # Shape: {'title1': {'all': 501, '2024': 501}, 'title2': {'all': 480, '2024': 480}, ...}
        views.update(
            view_bot.article_views_new(
                f"{lang}.wikipedia",
                titles,
                granularity="daily",
                start=start,
                end=END_DATE,
            )
        )

    return views


def split_views(
    lang: str,
    lang_views: dict[str, dict[str, int]],
    sql_values: dict[str, dict[str, int]],
) -> tuple[list[tuple], list[tuple]]:
    """Return (rows to insert, rows to update); a stored value is only ever raised, never lowered."""
    to_insert = []
    to_update = []

    for target, tab in lang_views.items():
        old_years = sql_values.get(target, {})

        for year, views in tab.items():
            # Skip the "all" total and years without views.
            if not str(year).isdigit() or views <= 0:
                continue

            year = str(year)

            if year not in old_years:
                to_insert.append((target, lang, year, views))
            elif views > (old_years[year] or 0):
                to_update.append((views, target, lang, year))

    return to_insert, to_update


def save_views(
    lang: str,
    lang_views: dict[str, dict[str, int]],
    sql_values: dict[str, Any],
) -> None:
    """Write the new and changed yearly views of one language to the database."""
    to_insert, to_update = split_views(lang, lang_views, sql_values)

    logger.info(f"{lang}: {len(to_insert)=}, {len(to_update)=}")

    for query, rows, size in (
        (UPDATE_QUERY, to_update, UPDATE_BATCH_SIZE),
        (INSERT_QUERY, to_insert, INSERT_BATCH_SIZE),
    ):
        for batch in batched(rows, size):
            sql_for_mdwiki.mdwiki_sql_update(query, values=batch, many=True)


def main() -> None:
    lang_to_targets = get_targets()
    already_in_sql = get_views_sql()

    view_bot = PageviewsClient()

    for lang, targets in lang_to_targets.items():
        lang_views = fetch_views(view_bot, lang, targets)

        save_views(lang, lang_views, already_in_sql.get(lang, {}))


if __name__ == "__main__":
    main()
