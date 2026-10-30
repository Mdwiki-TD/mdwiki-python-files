#!/usr/bin/python3
"""

python3 c9/pwb.py td_core/copy_data/by_title/all_articles

"""

import logging
from typing import Any

from db.mdapi_sql.sql_td_bot import tf_sql_connect_dict
from mdwiki_api.mdwiki_page import CatDepth

logger = logging.getLogger(__name__)


def insert_dict(
    list_of_lines,
    table_name: str,
    columns,
    lento: int = 10,
) -> None:

    logger.info(f"insert dict({table_name}): list_of_lines: {len(list_of_lines)}")

    if not list_of_lines:
        return

    done = 0

    # co_line = "title, importance"
    co_line = ", ".join(columns)
    values_line = ", ".join(["%s"] * len(columns))

    for i in range(0, len(list_of_lines), lento):
        tab = list_of_lines[i : i + lento]

        values = []

        for vav in tab:
            values_k = [vav.get(x, "") for x in columns]

            values_2 = []

            for value in values_k:
                # value = escape_string(value) if isinstance(value, str) else value

                values_2.append(value)

            values_2 = tuple(values_2)

            values.append(values_2)

        qua = f"""
            INSERT INTO {table_name} ({co_line})
            values ({values_line})
            """

        tf_sql_connect_dict(qua, values=values, many=True)

        done += len(tab)

        logger.info(f"to_sql.py insert dict({table_name}) {done} done, from {len(list_of_lines)} | batch: {lento}.")


def get_db_category_members() -> dict[str, list]:
    data: dict[str, list] = {}
    sql_result = tf_sql_connect_dict("select category, article_id from category_members;")

    for line in sql_result:
        if line["category"] not in data:
            data[line["category"]] = []
        data[line["category"]].append(line["article_id"])

    return data


def get_db_categories() -> dict[str, Any]:
    result = tf_sql_connect_dict("select category, depth from categories;")
    return {c["category"]: c["depth"] for c in result}


def main() -> None:
    # ---
    data = {}
    # ---
    length = {}
    # ---
    cats = get_db_categories()
    # ---
    if "RTT" in cats:
        del cats["RTT"]
    # ---
    videos_cats = ["Videowiki scripts", "RTTVideo"]
    # ---
    to_add_category_members = {}
    # ---
    for cat in cats.keys():
        # ---
        is_video_cat = cat in videos_cats or "video" in cat.lower()
        onlyns = 3000 if is_video_cat else ""
        ns = 3000 if is_video_cat else 0
        # ---
        mdwiki_pages = CatDepth(f"Category:{cat}", sitecode="www", family="mdwiki", depth=0, ns=ns, onlyns=onlyns)
        # ---
        titles = {dd: cat for dd in mdwiki_pages if dd not in data}
        # ---
        data.update(titles)
        # ---
        to_add_category_members[cat] = list(mdwiki_pages)
        # ---
        length[cat] = len(titles)
    # ---
    RTT_pages = CatDepth("Category:RTT", sitecode="www", family="mdwiki", depth=3, ns="0")
    # ---
    to_add_category_members["RTT"] = list(RTT_pages)
    # ---
    rtt_pages_subs = {title: "RTT" for title in RTT_pages if title not in data}
    # ---
    length["RTT"] = len(rtt_pages_subs)
    data.update(rtt_pages_subs)
    # ---s
    for cat, len_titles in length.items():
        logger.info(f"Category:{cat}: {len_titles=}")
    # ---
    # NOTE: previously this script also wrote a single-category-per-article
    # snapshot to `all_articles` via `start_to_sql(data)`. That table is being
    # retired in favour of the many-to-many `category_members` table populated
    # below, so the redundant write has been removed.
    add_category_members_to_sql(to_add_category_members)


def add_category_members_to_sql(to_add_category_members) -> None:
    # ---
    data2 = []
    # ---
    db_category_members = get_db_category_members()
    # ---
    for category, titles_from_mdwiki in to_add_category_members.items():
        # ---
        cats_in_db = db_category_members.get(category, [])
        # ---
        not_in = [
            {"category": category, "article_id": title} for title in titles_from_mdwiki if title not in cats_in_db
        ]
        # ---
        logger.info(f"Category:{category}: {len(titles_from_mdwiki)=}, {len(cats_in_db)=}")
        data2.extend(not_in)
    # ---
    insert_dict(
        data2,
        "category_members",
        ["article_id", "category"],
    )


if __name__ == "__main__":
    # ---
    main()
