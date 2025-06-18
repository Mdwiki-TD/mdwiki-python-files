#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/get_views_new

"""
import sys
import json
import time
from pathlib import Path
from newapi import printe
from newapi.mdwiki_page import user_agent

# from mwviews.api import PageviewsClient
from apis.mw_views import PageviewsClient
from update_med_views.helps import dump_one, load_lang_titles_from_dump

# Sends a descriptive User-Agent header with every request
view_bot = PageviewsClient(user_agent=user_agent)


def article_views_old(site, articles, year=2024):
    # ---
    time_start = time.time()
    # ---
    dd = view_bot.article_views(f'{site}.wikipedia', articles, granularity='monthly', start=f'{year}0101', end=f'{year}1231')
    # ---
    new_data = {}
    # ---
    for month, y in dd.items():
        # month = datetime.datetime(2024, 5, 1, 0, 0)
        year_n = month.strftime('%Y')
        for article, count in y.items():
            new_data.setdefault(article, {year_n: 0})
            if count:
                new_data[article][year_n] += count
    # ---
    delta = time.time() - time_start
    # ---
    printe.output(f"<<green>> article_views, (articles:{len(articles):,}) time: {delta:.2f} sec")
    # ---
    return new_data


def article_views(site, articles, year=2024):
    # ---
    new_data = view_bot.article_views_by_year(f'{site}.wikipedia', articles, granularity='monthly', start=f'{year}0101', end=f'{year}1231')
    # ---
    return new_data


def get_view_file(year, lang):
    # ---
    dir_v = Path(__file__).parent / "views" / str(year)
    # ---
    if not dir_v.exists():
        dir_v.mkdir(parents=True)
    # ---
    return dir_v / f"{lang}.json"


def get_one_lang_views_by_titles(langcode, titles, year):
    # ---
    all_data = {}
    # ---
    for i in range(0, len(titles), 50):
        # ---
        group = titles[i:i + 50]
        # ---
        data = article_views(langcode, group, year)
        # ---
        all_data.update(data)
    # ---
    return all_data


def load_one_lang_views(langcode, titles, year):
    # ---
    json_file = get_view_file(year, langcode)
    # ---
    if json_file.exists():
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    # ---
    if "local" in sys.argv:
        return {}
    # ---
    printe.output(f"<<green>> load_one_lang_views(lang:{langcode}) \t titles: {len(titles):,}")
    # ---
    data = get_one_lang_views_by_titles(langcode, titles, year)
    # ---
    dump_one(json_file, data)
    # ---
    return data


if __name__ == '__main__':
    # ---
    titles = load_lang_titles_from_dump("ba")
    # ---
    ux = article_views('ba', titles, 2024)
    # ---
    print(f"{len(ux)=:,}")
    # ---
    # article_views: time: 14.52 sec
