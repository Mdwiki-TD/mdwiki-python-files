#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/titles

from update_med_views.titles import load_one_lang_titles

"""
import sys
import json
from pathlib import Path
from update_med_views.helps import get_en_articles, langs_titles

t_dump_dir = Path(__file__).parent / "titles"
if not t_dump_dir.exists():
    t_dump_dir.mkdir()


def dump_data(all_data):
    # ---
    for n, (lang, titles) in enumerate(all_data.items(), start=1):
        # ---
        print(f"lang:{n}/{len(all_data)} \t {lang} {len(titles)}")
        # ---
        if not titles:
            continue
        # ---
        file = t_dump_dir / f"{lang}.json"
        # ---
        with open(file, "w", encoding="utf-8") as f:
            json.dump(titles, f, ensure_ascii=False)
    # ---
    print(f"dump_data: all langs: {len(all_data)}")


def load_one_lang_titles(lang):
    json_file = t_dump_dir / f"{lang}.json"
    # ---
    if not json_file.exists():
        return {}
    # ---
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def start():
    # ---
    # languages = count_all_langs()
    # ---
    all_links = langs_titles()
    # ---
    all_links["en"] = get_en_articles()
    # ---
    dump_data(all_links)


if __name__ == "__main__":
    start()
