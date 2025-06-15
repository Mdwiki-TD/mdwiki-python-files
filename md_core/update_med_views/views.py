#!/usr/bin/python3
"""

from update_med_views.views import get_one_lang_views_by_titles, load_one_lang_views

"""
import sys
import datetime
import json
import tqdm
from pathlib import Path

from apis import views_rest
# views_rest.get_views_with_rest_v1(langcode, titles, date_start="20150701", date_end="20300101", printurl=False, printstr=False, Type="daily")
# views_rest.get_views_last_30_days(langcode, titles)


v_dump_dir = Path(__file__).parent / "views"
if not v_dump_dir.exists():
    v_dump_dir.mkdir()


def views_dump_one(lang, titles):
    # ---
    print(f"lang:{lang}, {len(titles)}")
    # ---
    if not titles:
        return
    # ---
    file = v_dump_dir / f"{lang}.json"
    # ---
    with open(file, "w", encoding="utf-8") as f:
        json.dump(titles, f, ensure_ascii=False)


def get_one_lang_views_by_titles(langcode, titles, year):
    # ---
    total = 0
    # ---
    data = views_rest.get_views_with_rest_v1(langcode, titles, date_start=f"{year}0101", date_end=f"{year}1231", printurl=False, printstr=False, Type="daily")
    # ---
    for _, tab in tqdm.tqdm(data.items()):
        total += tab["all"]
    # ---
    return total


def load_one_lang_views(langcode, titles, year):
    # ---
    json_file = v_dump_dir / f"{langcode}.json"
    # ---
    if not json_file.exists():
        # ---
        data = get_one_lang_views_by_titles(langcode, titles, year)
        # ---
        views_dump_one(langcode, data)
        # ---
        return data
    # ---
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)
