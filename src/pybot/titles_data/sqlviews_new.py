#!/usr/bin/python3
"""
page views_new bot

python3 c9/pwb.py titles_data/sqlviews_new -lang:ga

USED IN mdwiki-jobs.yaml
"""

import copy
import logging
import re

from db.mdapi_sql.services import sql_for_mdwiki
from db.to_sql_new import insert_dict, update_table
from md_core_helps.apis.mw_views import PageviewsClient

logger = logging.getLogger(__name__)

# new_data = view_bot.article_views_new(f'{site}.wikipedia', ["title1", "title2"], granularity='monthly', start=f'{year}0101', end=f'{year}1231')
# {'title1': {'all': 501, '2024': 501}, 'title2': {'all': 480, '2024': 480}, ... }


def update_in_sql(lang, table, already_in_sql) -> None:

    logger.info("update_in_sql:")

    sql_values = already_in_sql.get(lang, {})

    to_insert = []

    new_data = []

    for target, tab in table.items():
        sq = sql_values.get(target, {})

        if "all" in tab:
            del tab["all"]

        years = {str(y): x for y, x in tab.items() if str(y).isdigit() and x > 0}

        years2 = copy.deepcopy(years)

        for y, views in years2.items():
            if not sq.get(y):
                to_insert.append({"target": target, "lang": lang, "year": y, "views": views})
            elif sq.get(y, 0) > views:
                years[y] = sq.get(y, 0)

        if all(sq.get(str(year), 0) == years.get(str(year), 0) for year in years.keys()):
            logger.debug(f"page:{target} has same views_new.. skip")
            continue

        new_data.extend([{"target": target, "lang": lang, "year": x, "views": views} for x, views in years.items()])

    update_table(
        new_data,
        "views_new",
        columns_to_set=["views"],
        columns_where=["target", "lang", "year"],
    )

    insert_dict(
        list_of_lines=to_insert,
        table_name="views_new",
        columns=["target", "lang", "year", "views"],
        lento=1000,
        ignore=True,
    )


def get_targets():

    que = 'select DISTINCT lang, target, pupdate from pages where target != ""'

    sq = sql_for_mdwiki.mdwiki_sql_dict(que)

    lang_to_targets = {}
    for tab in sq:
        lang = tab["lang"].lower()
        target = tab["target"]
        pupdate = tab["pupdate"]

        if target != "":
            if lang not in lang_to_targets:
                lang_to_targets[lang] = {}
            lang_to_targets[lang][target] = pupdate

    logger.info(f"find {len(sq)} to work. ")
    return lang_to_targets


def get_views_sql():

    que11 = """select DISTINCT target, lang, year, views from views_new"""

    dad = sql_for_mdwiki.mdwiki_sql_dict(que11)

    already_in_sql = {}
    for tab in dad:
        target = tab["target"]
        lang = tab["lang"].lower()
        views = tab["views"]
        year = tab["year"]

        if lang not in already_in_sql:
            already_in_sql[lang] = {}

        if target not in already_in_sql[lang]:
            already_in_sql[lang][target] = {}

        already_in_sql[lang][target][str(year)] = views

    return already_in_sql


def main() -> None:
    logger.info(" _finder: ")

    lang_to_targets = get_targets()
    already_in_sql = get_views_sql()

    lang_pupdate_titles = {}

    for lang, tit_list in lang_to_targets.items():
        if lang not in lang_pupdate_titles:
            lang_pupdate_titles[lang] = {}

        # قوائم حسب تاريخ النشر
        for tit, pupdate in tit_list.items():
            if pupdate not in lang_pupdate_titles[lang]:
                lang_pupdate_titles[lang][pupdate] = []

            lang_pupdate_titles[lang][pupdate].append(tit)

    view_bot = PageviewsClient()

    for lange, tab in lang_pupdate_titles.items():
        numbs = {}

        for pupdate, title_list in tab.items():
            start = "20210401"

            rem = re.match(r"^(?P<y>\d\d\d\d)-(?P<m>\d\d)-(?P<d>\d\d)$", pupdate)

            if rem:
                start = rem.group("y") + rem.group("m") + rem.group("d")

            lenlist = len(title_list)

            logger.info("---")
            logger.info(f"get pageviews for {lenlist} pages, date_start:{start}")

            if lenlist < 5:
                logger.info(", ".join(title_list))

            new_data = view_bot.article_views_new(
                f"{lange}.wikipedia",
                title_list,
                granularity="daily",
                start=start,
                end="20300101",
            )

            # {'title1': {'all': 501, '2024': 501}, 'title2': {'all': 480, '2024': 480}, ... }

            numbs = {**numbs, **new_data}

        update_in_sql(lange, numbs, already_in_sql)


if __name__ == "__main__":
    main()
