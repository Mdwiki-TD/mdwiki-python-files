#!/usr/bin/python3
"""

from update_med_views.views import get_one_lang_views_by_titles, load_one_lang_views

"""
import sys
import datetime
import json
import tqdm
from pathlib import Path
from update_med_views.helps import dump_one
from apis import views_rest
# views_rest.get_views_with_rest_v1(langcode, titles, date_start="20150701", date_end="20300101", printurl=False, printstr=False, Type="daily")
# views_rest.get_views_last_30_days(langcode, titles)


v_dump_dir = Path(__file__).parent / "views"
if not v_dump_dir.exists():
    v_dump_dir.mkdir()


def get_one_lang_views_by_titles(langcode, titles, year):
    # ---
    all_data = {}
    # ---
    for i in range(0, len(titles), 50):
        # ---
        group = titles[i:i + 50]
        # ---
        data = views_rest.get_views_with_rest_v1(langcode, group, date_start=f"{year}0101", date_end=f"{year}1231", printurl=False, printstr=False, Type="daily")
        # ---
        all_data.update(data)
    # ---
    return all_data


def load_one_lang_views(langcode, titles, year):
    # ---
    json_file = v_dump_dir / f"{langcode}.json"
    # ---
    if json_file.exists():
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    # ---
    if "local" in sys.argv:
        return {}
    # ---
    data = get_one_lang_views_by_titles(langcode, titles, year)
    # ---
    file = v_dump_dir / f"{langcode}.json"
    # ---
    dump_one(file, data)
    # ---
    return data
