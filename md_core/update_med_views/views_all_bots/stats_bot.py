#!/usr/bin/python3
"""

from update_med_views.views_all_bots.helps import json_load, get_views_all_file, update_data_new

"""
from update_med_views.views_all_bots.helps import is_empty_data
from update_med_views.helps import dump_one


def sum_all_views(new_data):
    # all_keys = []
    # for x in new_data.values(): all_keys.extend(x.keys())
    # all_keys = list(set(all_keys))
    # ---
    all_keys = list(set().union(*map(dict.keys, new_data.values())))
    all_keys.sort()
    # ---
    views = {}
    # ---
    for year in all_keys:
        views[year] = sum(x.get(year, 0) for x in new_data.values())
    # ---
    return views


def sum_all_views_new(new_data):
    views = {}
    for x in new_data.values():
        for k, v in x.items():
            views[k] = views.get(k, 0) + v

    views = dict(sorted(views.items()))
    return views


def dump_stats(json_file_stats, new_data):
    # ---
    data_hash = [x for x in new_data if x.find("#") != -1]
    # ---
    data2 = {x: new_data[x] for x in new_data if x not in data_hash}
    # ---
    empty = [x for x in data2.values() if is_empty_data(x)]
    # ---
    views = sum_all_views(new_data)
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
