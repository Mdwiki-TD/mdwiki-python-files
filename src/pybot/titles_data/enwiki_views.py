#!/usr/bin/python3
"""
إنشاء قائمة بمشاهدات المقالات من الانجليزية

وحفظها في قاعدة البيانات

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

    en_keys = [re.sub(r"^Video:", "Wikipedia:VideoWiki/", x, flags=re.IGNORECASE) for x in en_keys]

    view_bot = PageviewsClient()

    enviews = view_bot.article_views_new("en.wikipedia", en_keys)

    # {'Yemen': {'all': 187379, '2025': 187379}, 'COVID-19': {'all': 230007, '2025': 230007}}

    enviews_0 = {k: v for k, v in enviews.items() if v.get("all", 0) == 0}

    logger.info(f"<<purple>> len of enviews: {len(enviews.keys())}, len of enviews_0: {len(enviews_0.keys())}")

    data: dict[str, int] = {}
    no_views = 0

    for k, view in enviews.items():
        view_all = view.get("all", 0)

        if view_all == 0 or view_all == "0" or not view_all:
            no_views += 1
            continue

        k = k.replace("Wikipedia:VideoWiki/", "Video:")
        k = enwiki_to_mdwiki.get(k) or k

        data[k] = view_all

    logger.info(f"no_views:{no_views},\t len of old_values: {len(data.keys())}")

    return data


def save_to_sql(data, from_sql) -> None:
    tab = [{"title": x, "en_views": v} for x, v in data.items()]

    new_to_sql(
        data=tab,
        table_name="enwiki_pageviews",
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
