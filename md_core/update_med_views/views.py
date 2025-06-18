#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/views

"""
import sys
import json
import time
from pathlib import Path
from newapi import printe

# from mwviews.api import PageviewsClient
from apis.mw_views import PageviewsClient
from update_med_views.helps import dump_one, load_lang_titles_from_dump

# Sends a descriptive User-Agent header with every request
view_bot = PageviewsClient()


def article_views(site, articles, year=2024):
    # ---
    new_data = view_bot.article_views_new(f'{site}.wikipedia', articles, granularity='monthly', start=f'{year}0101', end=f'{year}1231')
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
    in_file = {}
    # ---
    if json_file.exists():
        # ---
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        # ---
        printe.output(f"<<green>> load_one_lang_views(lang:{langcode}) \t from file: {json_file}, titles: {len(titles):,}")
        # ---
        titles_not_in_file = [x for x in titles if x not in data]
        # ---
        if len(data) != len(titles) or len(titles_not_in_file) > 0:
            printe.output(f"<<red>> titles: {len(titles):,}, titles in file: {len(data):,}, missing: {len(titles_not_in_file):,}")
            in_file = data
            # ---
            titles = titles_not_in_file
        else:
            return data
    # ---
    if "local" in sys.argv:
        return {}
    # ---
    printe.output(f"<<green>> load_one_lang_views(lang:{langcode}) \t titles: {len(titles):,}")
    # ---
    data = get_one_lang_views_by_titles(langcode, titles, year)
    # ---
    if len(in_file) > 0:
        # ---
        printe.output(f"<<yellow>> new data: {len(data)}, in_file: {len(in_file)}")
        # ---
        data.update(in_file)
    # ---
    dump_one(json_file, data)
    # ---
    return data


if __name__ == '__main__':
    # ---
    # titles = load_lang_titles_from_dump("ba")
    # ---
    # ux = article_views('ba', titles, 2024)
    # ---
    titles = ["Yemen", "COVID-19"]
    # ---
    zz = view_bot.article_views_new('en.wikipedia', titles)
    # ---
    print(zz)
    print(f"{len(zz)=:,}")
    # ---
    # article_views: time: 14.52 sec
