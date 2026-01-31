#!/usr/bin/python3
"""
page views_new bot

python3 core8/pwb.py mdpyget/sqlviews_new -lang:ga

"""

import copy
import logging
import re
import sys

from apis.mw_views import PageviewsClient
from mdapi_sql import sql_for_mdwiki
from mdpyget.bots.to_sql import insert_dict, update_table_2

logger = logging.getLogger(__name__)

view_bot = PageviewsClient()
# new_data = view_bot.article_views_new(f'{site}.wikipedia', ["title1", "title2"], granularity='monthly', start=f'{year}0101', end=f'{year}1231')
# {'title1': {'all': 501, '2024': 501}, 'title2': {'all': 480, '2024': 480}, ... }

already_in_sql = {}
Lang_to_targets = {}


def print_test(strr):
    if "print" in sys.argv or "nosql" in sys.argv:
        logger.info(strr)


def update_in_sql(lang, table):
    # ---
    print("update_in_sql:")
    # ---
    sql_values = already_in_sql.get(lang, {})
    # ---
    to_insert = []
    # ---
    new_data = []
    # ---
    for target, tab in table.items():
        # ---
        sq = sql_values.get(target, {})
        # ---
        if "all" in tab:
            del tab["all"]
        # ---
        # years = {str(y) : x["all"] for y, x in tab.items() if str(y).isdigit() and x["all"] > 0}
        years = {str(y): x for y, x in tab.items() if str(y).isdigit() and x > 0}
        # ---
        years2 = copy.deepcopy(years)
        # ---
        for y, views in years2.items():
            if not sq.get(y):
                to_insert.append({"target": target, "lang": lang, "year": y, "views": views})
            elif sq.get(y, 0) > views:
                years[y] = sq.get(y, 0)
        # ---
        if all(sq.get(str(year), 0) == years.get(str(year), 0) for year in years.keys()):
            print_test(f"page:{target} has same views_new.. skip")
            continue
        # ---
        new_data.extend([{"target": target, "lang": lang, "year": x, "views": views} for x, views in years.items()])
    # ---
    update_table_2(new_data, "views_new", columns_to_set=["views"], columns_where=["target", "lang", "year"])
    # ---
    insert_dict(
        to_insert, "views_new", ["target", "lang", "year", "views"], lento=1000, title_column="target", IGNORE=True
    )


def insert_to_sql(lang, table):
    # ---
    for target, tab in table.items():
        # ---
        if "all" in tab:
            del tab["all"]
        # ---
        # years = {y : x["all"] for y, x in tab.items() if y.isdigit() and x["all"] > 0}
        years = {y: x for y, x in tab.items() if y.isdigit() and x > 0}
        # ---
        data_list = [{"target": target, "lang": lang, "year": x, "views": views} for x, views in years.items()]
        # ---
        insert_dict(
            data_list, "views_new", ["target", "lang", "year", "views"], lento=1000, title_column="target", IGNORE=True
        )


def get_targets(lang_o):
    uu = f'and lang = "{lang_o}"' if lang_o != "" else ""
    # ---
    que = f"""select DISTINCT lang, target, pupdate from pages where target != "" {uu}"""
    # ---
    sq = sql_for_mdwiki.select_md_sql(que, return_dict=True)
    # ---
    for tab in sq:
        lang = tab["lang"].lower()
        target = tab["target"]
        pupdate = tab["pupdate"]
        # ---
        if target != "":
            if lang not in Lang_to_targets:
                Lang_to_targets[lang] = {}
            Lang_to_targets[lang][target] = pupdate
    # ---
    print(f"<<yellow>> find {len(sq)} to work. ")


def get_views_sql(lang_o):
    # ---
    uu = f'where lang = "{lang_o}"' if lang_o != "" else ""
    # ---
    que11 = f"""select DISTINCT target, lang, year, views from views_new {uu}"""
    # ---
    dad = sql_for_mdwiki.select_md_sql(que11, return_dict=True)
    # ---
    for tab in dad:
        # ---
        target = tab["target"]
        lang = tab["lang"].lower()
        views = tab["views"]
        year = tab["year"]
        # ---
        if lang not in already_in_sql:
            already_in_sql[lang] = {}
        # ---
        if target not in already_in_sql[lang]:
            already_in_sql[lang][target] = {}
        # ---
        already_in_sql[lang][target][str(year)] = views


def main():
    # ---
    print(" _finder: ")
    # ---
    lang_o = ""
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg in ["lang", "-lang"]:
            lang_o = value
    # ---
    get_targets(lang_o)
    # ---
    get_views_sql(lang_o)
    # ---
    lang_pupdate_titles = {}
    # ---
    for lang, tit_list in Lang_to_targets.items():
        # ---
        if lang not in lang_pupdate_titles:
            lang_pupdate_titles[lang] = {}
        # ---
        # قوائم حسب تاريخ النشر
        for tit, pupdate in tit_list.items():
            # ---
            if pupdate not in lang_pupdate_titles[lang]:
                lang_pupdate_titles[lang][pupdate] = []
            # ---
            lang_pupdate_titles[lang][pupdate].append(tit)
    # ---
    for lange, tab in lang_pupdate_titles.items():
        # ---
        numbs = {}
        # ---
        for pupdate, title_list in tab.items():
            start = "20210401"
            # ---
            rem = re.match(r"^(?P<y>\d\d\d\d)-(?P<m>\d\d)-(?P<d>\d\d)$", pupdate)
            # ---
            if rem:
                start = rem.group("y") + rem.group("m") + rem.group("d")
            # ---
            lenlist = len(title_list)
            # ---
            logger.info("---")
            logger.info(f"<<yellow>> get pageviews for {lenlist} pages, date_start:{start}")
            # ---
            if lenlist < 5:
                logger.info(", ".join(title_list))
            # ---
            new_data = view_bot.article_views_new(
                f"{lange}.wikipedia", title_list, granularity="daily", start=start, end="20300101"
            )
            # ---
            # {'title1': {'all': 501, '2024': 501}, 'title2': {'all': 480, '2024': 480}, ... }
            # ---
            numbs = {**numbs, **new_data}
        # ---
        if "testtest" in sys.argv:
            continue
        # ---
        insert = {}
        update = {}
        # ---
        sql_values = already_in_sql.get(lange, {})
        # ---
        for target, tab in numbs.items():
            # ---
            if sql_values.get(target, {}) != {}:
                update[target] = tab
            else:
                insert[target] = tab
        # ---
        update_in_sql(lange, numbs)
        # ---
        # insert_to_sql(lange, insert)


if __name__ == "__main__":
    main()
