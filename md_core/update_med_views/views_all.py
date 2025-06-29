#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/views_all

"""
import sys
import json
from pathlib import Path
from newapi import printe

from apis.mw_views import PageviewsClient
from update_med_views.helps import dump_one

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


def is_empty_data(data):
    # ---
    # print(data)
    # ---
    if not data:
        return True
    # ---
    if data.get("all", 0) == 0:
        return True
    # ---
    if len(data) == 1:
        return True
    # ---
    # if any of values is 0
    # if any([x == 0 for x in data.values()]): return True
    # ---
    return False


def dump_hash(json_file_stats, new_data):
    # ---
    data_hash = [x for x in new_data if x.find("#") != -1]
    # ---
    data2 = {x: new_data[x] for x in new_data if x not in data_hash}
    # ---
    empty = [x for x in data2.values() if is_empty_data(x)]
    # ---
    views = {
        "all": sum(x.get("all", 0) for x in new_data.values()),
        "2024": sum(x.get("2024", 0) for x in new_data.values())
    }
    # ---
    stats = {
        "all": len(data2),
        "empty": len(empty),
        "not_empty": len(data2) - len(empty),
        "hash": len(data_hash),
        "views": views
    }
    # ---
    print(stats)
    # ---
    dump_one(json_file_stats, stats)
    # ---
    return stats


def dump_it(json_file, data, json_file_stats):
    # ---
    new_data = {}
    # ---
    # sort all sub data inside data
    for k, v in data.items():
        new_data[k] = {k2: v2 for k2, v2 in sorted(v.items(), key=lambda item: item[0], reverse=False)}
    # ---
    dump_one(json_file, new_data)
    # ---
    dump_hash(json_file_stats, new_data)


def article_all_views(site, articles, year=2024):
    # ---
    site = 'be-tarask' if site == 'be-x-old' else site
    # ---
    data = view_bot.article_views_new(f'{site}.wikipedia', articles, granularity='monthly', start='20100101', end='20250627')
    # ---
    # print(data)
    # ---
    return data


def get_views_all_file(lang, subdir="all"):
    # ---
    dir_v = Path(__file__).parent / "views_new" / subdir
    # ---
    if not dir_v.exists():
        dir_v.mkdir(parents=True)
    # ---
    file = dir_v / f"{lang}.json"
    # ---
    return file


def update_data_new(all_data, data):
    # ---
    for title, counts in data.items():
        all_data.setdefault(title, {})
        # ---
        all_data[title].update({x: v for x, v in counts.items() if (x not in all_data[title] or all_data[title][x] == 0)})
    # ---
    return all_data


def get_one_lang_views_all_by_titles(langcode, titles, year):
    # ---
    all_data = {}
    # ---
    for i in range(0, len(titles), 20):
        # ---
        group = titles[i:i + 20]
        # ---
        data = article_all_views(langcode, group, year)
        # ---
        all_data = update_data_new(all_data, data)
    # ---
    return all_data


def get_one_lang_views_all_by_titles_plus_1k(langcode, titles, year, json_file, json_file_stats, max_items=1000):
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
        data = article_all_views(langcode, group, year)
        # ---
        all_data = update_data_new(all_data, data)
        # ---
        in_file = update_data_new(in_file, data)
        # ---
        dump_it(json_file, in_file, json_file_stats)
    # ---
    return all_data


def render_data(titles, langcode, year, json_file, json_file_stats, max_items=1000):
    data = {}
    # ---
    if "zero" in sys.argv:
        data = {x: {"all": 0} for x in titles}
    elif len(titles) > max_items:
        data = get_one_lang_views_all_by_titles_plus_1k(langcode, titles, year, json_file, json_file_stats, max_items=max_items)
    else:
        data = get_one_lang_views_all_by_titles(langcode, titles, year)
    # ---
    data = {x.replace("_", " "): v for x, v in data.items()}
    # ---
    return data


def get_titles_and_in_file(json_file, titles):
    # ---
    if not json_file.exists():
        print("json_file does not exist")
        return titles, {}
    # ---
    u_data = json_load(json_file)
    # ---
    if u_data is False:
        # TODO: error when loading the json data
        return [], {}
    # ---
    titles_not_in_file = [x for x in titles if is_empty_data(u_data.get(x, {})) and x.find("#") == -1]
    # ---
    if not (len(u_data) != len(titles) or len(titles_not_in_file) > 0):
        printe.output(f"<<green>> load_one_lang_views_all(lang:{json_file}) \t titles: {len(titles):,}")
        print("nothing to do")
        return [], {}
    # ---
    printe.output(f"<<red>>(lang:{json_file.name}) titles: {len(titles):,}, titles in file: {len(u_data):,}, missing: {len(titles_not_in_file):,}")
    # ---
    in_file = u_data
    # ---
    titles = titles_not_in_file
    # ---
    return titles, in_file


def get_titles_to_work(langcode, titles, year):
    # ---
    json_file = get_views_all_file(langcode)
    # ---
    titles_to_work, _ = get_titles_and_in_file(json_file, titles)
    # ---
    if titles_to_work == titles:
        return []
    # ---
    return titles_to_work


def load_one_lang_views_all(langcode, titles, year, max_items=1000, maxv=0):
    # ---
    json_file = get_views_all_file(langcode)
    json_file_stats = get_views_all_file(langcode, "stats")
    # ---
    titles, in_file = get_titles_and_in_file(json_file, titles)
    # # ---
    if len(titles) == 0:
        return
    # ---
    if maxv > 0 and len(titles) > maxv:
        printe.output(f"<<yellow>> {langcode}: {len(titles)} titles > max {maxv}, skipping")
        return
    # ---
    if "local" in sys.argv:
        return
    # ---
    data = render_data(titles, langcode, year, json_file, json_file_stats, max_items=1000)
    # ---
    if len(in_file) > 0:
        # ---
        printe.output(f"<<yellow>>(lang:{langcode}) new data: {len(data)}, in_file: {len(in_file)}")
        # ---
        data = update_data_new(in_file, data)
    else:
        printe.output(f"<<green>>(lang:{langcode}) new data: {len(data)}")
    # ---
    dump_it(json_file, data, json_file_stats)
