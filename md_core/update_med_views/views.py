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
    for i in range(0, len(titles), 1000):
        # ---
        group = titles[i:i + 1000]
        # ---
        data = article_views(langcode, group, year)
        # ---
        all_data.update({x: v for x, v in data.items() if x not in all_data})
    # ---
    return all_data


def get_one_lang_views_by_titles_plus_1k(langcode, titles, year, json_file):
    # ---
    in_file = {}
    all_data = {}
    # ---
    if json_file.exists():
        with open(json_file, "r", encoding="utf-8") as f:
            in_file = json.load(f)
    # ---
    for i in range(0, len(titles), 1000):
        # ---
        group = titles[i:i + 1000]
        # ---
        data = article_views(langcode, group, year)
        # ---
        all_data.update({x: v for x, v in data.items() if x not in all_data})
        # ---
        in_file.update({x: v for x, v in data.items() if x not in in_file})
        # ---
        dump_one(json_file, in_file)
    # ---
    return all_data


def load_one_lang_views(langcode, titles, year):
    # ---
    json_file = get_view_file(year, langcode)
    # ---
    u_data = {}
    in_file = {}
    # ---
    if json_file.exists():
        # ---
        with open(json_file, "r", encoding="utf-8") as f:
            u_data = json.load(f)
        # ---
        # printe.output(f"<<green>> load_one_lang_views(lang:{langcode}) \t from file: {json_file.name}, titles: {len(titles):,}")
        # ---
        titles_not_in_file = [x for x in titles if x not in u_data]
        # ---
        if len(u_data) != len(titles) or len(titles_not_in_file) > 0:
            printe.output(f"<<red>>(lang:{langcode}) titles: {len(titles):,}, titles in file: {len(u_data):,}, missing: {len(titles_not_in_file):,}")
            in_file = u_data
            # ---
            titles = titles_not_in_file
        else:
            printe.output(f"<<green>> load_one_lang_views(lang:{langcode}) \t titles: {len(titles):,}")
            # ---
            return u_data
    # ---
    if "local" in sys.argv:
        return {}
    # ---
    if len(titles) > 1000:
        data = get_one_lang_views_by_titles_plus_1k(langcode, titles, year, json_file)
    else:
        data = get_one_lang_views_by_titles(langcode, titles, year)
    # ---
    if len(in_file) > 0:
        # ---
        printe.output(f"<<yellow>>(lang:{langcode}) new data: {len(data)}, in_file: {len(in_file)}")
        # ---
        data.update({x: v for x, v in in_file.items() if x not in data})
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
