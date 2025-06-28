#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/views_all

"""
import sys
import json
from pathlib import Path
from newapi import printe


# from mwviews.api import PageviewsClient
from apis.mw_views import PageviewsClient
from update_med_views.helps import dump_one, load_lang_titles_from_dump
from update_med_views.helps import load_languages_counts

# Sends a descriptive User-Agent header with every request

parallelism = 2

for arg in sys.argv:
    key, _, val = arg.partition(':')
    if key == '-para':
        parallelism = int(val) or parallelism

view_bot = PageviewsClient(parallelism=parallelism)


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
    if any([x == 0 for x in data.values()]):
        return True
    # ---
    return False


def dump_it(json_file, data):
    # ---
    new_data = {}
    # ---
    # sort all sub data inside data
    for k, v in data.items():
        new_data[k] = {k2: v2 for k2, v2 in sorted(v.items(), key=lambda item: item[0], reverse=False)}
    # ---
    return dump_one(json_file, new_data)


def article_all_views(site, articles, year=2024):
    # ---
    data = view_bot.article_views_new(f'{site}.wikipedia', articles, granularity='monthly', start='20100101', end='20241231')
    # ---
    # print(data)
    # ---
    return data


def get_views_all_file(lang, year, open_it=False):
    # ---
    dir_v = Path(__file__).parent / "views_new" / "all"
    # ---
    if not dir_v.exists():
        dir_v.mkdir(parents=True)
    # ---
    file = dir_v / f"{lang}.json"
    # ---
    if open_it:
        if file.exists():
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}
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


def get_one_lang_views_all_by_titles_plus_1k(langcode, titles, year, json_file, max_items=1000):
    # ---
    in_file = {}
    all_data = {}
    # ---
    if json_file.exists():
        with open(json_file, "r", encoding="utf-8") as f:
            in_file = json.load(f)
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
        dump_it(json_file, in_file)
    # ---
    return all_data


def load_one_lang_views_all(langcode, titles, year, max_items=1000, maxv=0):
    # ---
    json_file = get_views_all_file(langcode, year)
    # ---
    u_data = {}
    in_file = {}
    # ---
    titles = [x.replace("_", " ") for x in titles]
    # ---
    if json_file.exists():
        # ---
        with open(json_file, "r", encoding="utf-8") as f:
            u_data = json.load(f)
        # ---
        u_data = {x.replace("_", " "): v for x, v in u_data.items()}
        # ---
        titles_not_in_file = [x for x in titles if is_empty_data(u_data.get(x, {}))]
        # ---
        if len(u_data) != len(titles) or len(titles_not_in_file) > 0:
            printe.output(f"<<red>>(lang:{json_file.name}) titles: {len(titles):,}, titles in file: {len(u_data):,}, missing: {len(titles_not_in_file):,}")
            # ---
            in_file = u_data
            # ---
            titles = titles_not_in_file
        else:
            printe.output(f"<<green>> load_one_lang_views_all(lang:{json_file}) \t titles: {len(titles):,}")
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
        data = {x: {"all": 0} for x in titles}
    elif len(titles) > max_items:
        data = get_one_lang_views_all_by_titles_plus_1k(langcode, titles, year, json_file, max_items=max_items)
    else:
        data = get_one_lang_views_all_by_titles(langcode, titles, year)
    # ---
    data = {x.replace("_", " "): v for x, v in data.items()}
    # ---
    if len(in_file) > 0:
        # ---
        printe.output(f"<<yellow>>(lang:{langcode}) new data: {len(data)}, in_file: {len(in_file)}")
        # ---
        in_file = update_data_new(in_file, data)
        # ---
        dump_it(json_file, in_file)
        # ---
        data = in_file
    else:
        # ---
        printe.output(f"<<green>>(lang:{langcode}) new data: {len(data)}")
        # ---
        dump_it(json_file, data)
    # ---
    return data


def start():
    # python3 core8/pwb.py update_med_views/views_all start
    langs = load_languages_counts()
    # ---
    # sort langs by len of titles { "ar": 19972, "bg": 2138, .. }
    langs = dict(sorted(langs.items(), key=lambda item: item[1], reverse=False))
    # ---
    for lang, length in langs.items():
        titles = load_lang_titles_from_dump(lang)
        # ---
        if len(titles) == 0:
            continue
        # ---
        printe.output(f"<<yellow>>lang:{lang}, {length:,}\ttitles: {len(titles)}")
        # ---
        if "no" not in sys.argv:
            data = load_one_lang_views_all(lang, titles, "all")


def test2():
    # python3 core8/pwb.py update_med_views/views_all test2
    titles = ["Yemen", "COVID-19", "Iran–Israel war", "wj2340-0"]
    # ---
    ux = article_all_views('en', titles, 2024)
    # ---
    for t, tt in ux.items():
        print(t, tt)
    # ---
    print(f"{len(ux)=:,}")


def test():
    # python3 core8/pwb.py update_med_views/views_all test
    titles = load_lang_titles_from_dump("ar")
    data = load_one_lang_views_all("ar", titles, "all")


if __name__ == '__main__':
    # ---
    defs = {
        "start": start,
        "test2": test2,
        "test": test,
    }
    # ---
    for arg in sys.argv:
        if arg in defs:
            defs[arg]()
