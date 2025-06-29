#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/views

"""
import sys
import json
from pathlib import Path
from newapi import printe

# from mwviews.api import PageviewsClient
from apis.mw_views import PageviewsClient
from update_med_views.helps import dump_one, load_lang_titles_from_dump

# Sends a descriptive User-Agent header with every request

parallelism = 2

for arg in sys.argv:
    key, _, val = arg.partition(':')
    if key == '-para':
        parallelism = int(val) or parallelism

view_bot = PageviewsClient(parallelism=parallelism)


def json_load(json_file):
    # ---
    u_data = False
    # ---
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            u_data = json.load(f)
    except Exception as e:
        printe.output(f"<<red>> json_load({json_file}) {e}")
    # ---
    if isinstance(u_data, dict):
        u_data = {x.replace("_", " "): v for x, v in u_data.items()}
    elif isinstance(u_data, list):
        u_data = [x.replace("_", " ") for x in u_data]
    # ---
    return u_data


def article_views(site, articles, year=2024):
    # ---
    data = view_bot.article_views_new(f'{site}.wikipedia', articles, granularity='monthly', start=f'{year}0101', end=f'{year}1231')
    # ---
    new_data = {}
    # ---
    for title, views in data.items():
        # ---
        title = title.replace(" ", "_")
        # ---
        new_data[title] = views.get(year) or views.get(str(year)) or views.get('all', 0)
    # ---
    return new_data


def get_view_file(lang, year, open_it=False):
    # ---
    dir_v = Path(__file__).parent / "views" / str(year)
    # ---
    if not dir_v.exists():
        dir_v.mkdir(parents=True)
    # ---
    file = dir_v / f"{lang}.json"
    # ---
    if open_it:
        data = json_load(file)
        # ---
        if data is False:
            return False
    # ---
    return file


def update_data(all_data, data):
    # ---
    all_data.update({x: v for x, v in data.items() if (x not in all_data or all_data[x] == 0)})
    # ---
    return all_data


def get_one_lang_views_by_titles(langcode, titles, year):
    # ---
    all_data = {}
    # ---
    for i in range(0, len(titles), 20):
        # ---
        group = titles[i:i + 20]
        # ---
        data = article_views(langcode, group, year)
        # ---
        all_data = update_data(all_data, data)
    # ---
    return all_data


def get_one_lang_views_by_titles_plus_1k(langcode, titles, year, json_file, max_items=1000):
    # ---
    in_file = {}
    all_data = {}
    # ---
    if json_file.exists():
        in_file = json_load(json_file)
    # ---
    if in_file is False:
        return False
    # ---
    for i in range(0, len(titles), 200):
        # ---
        group = titles[i:i + 200]
        # ---
        data = article_views(langcode, group, year)
        # ---
        all_data = update_data(all_data, data)
        # ---
        in_file = update_data(in_file, data)
        # ---
        dump_one(json_file, in_file)
    # ---
    return all_data


def load_one_lang_views(langcode, titles, year, max_items=1000, maxv=0):
    # ---
    json_file = get_view_file(langcode, year)
    # ---
    u_data = {}
    in_file = {}
    # ---
    if json_file.exists():
        # ---
        u_data = json_load(json_file)
        # ---
        if u_data is False:
            return False
        # ---
        u_data = {x.replace("_", " "): v for x, v in u_data.items()}
        # ---
        titles_not_in_file = [x for x in titles if (x not in u_data or u_data[x] == 0)]
        # ---
        if len(u_data) != len(titles) or len(titles_not_in_file) > 0:
            printe.output(f"<<red>>(lang:{json_file.name}) titles: {len(titles):,}, titles in file: {len(u_data):,}, missing: {len(titles_not_in_file):,}")
            # ---
            in_file = u_data
            # ---
            titles = titles_not_in_file
        else:
            printe.output(f"<<green>> load_one_lang_views(lang:{json_file}) \t titles: {len(titles):,}")
            # ---
            return u_data
    # ---
    if maxv > 0 and len(titles) > maxv:
        printe.output(f"<<yellow>> {langcode}: {len(titles)} titles > max {maxv}, skipping")
        return u_data
    # ---
    if "local" in sys.argv:
        return u_data
    # ---
    if "zero" in sys.argv:
        data = {x: 0 for x in titles}
    elif len(titles) > max_items:
        data = get_one_lang_views_by_titles_plus_1k(langcode, titles, year, json_file, max_items=max_items)
    else:
        data = get_one_lang_views_by_titles(langcode, titles, year)
    # ---
    data = {x.replace("_", " "): v for x, v in data.items()}
    # ---
    if len(in_file) > 0:
        # ---
        printe.output(f"<<yellow>>(lang:{langcode}) new data: {len(data)}, in_file: {len(in_file)}")
        # ---
        in_file = update_data(in_file, data)
        # ---
        dump_one(json_file, in_file)
        # ---
        data = in_file
    else:
        # ---
        printe.output(f"<<green>>(lang:{langcode}) new data: {len(data)}")
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
