#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/titles

from update_med_views.titles import load_lang_titles

"""
import sys
import json
from update_med_views.helps import t_dump_dir, langs_titles, one_lang_titles, dump_one, load_lang_titles_from_dump


def dump_data(all_data):
    # ---
    for n, (lang, titles) in enumerate(all_data.items(), start=1):
        # ---
        print(f"dump_data(): lang:{n}/{len(all_data)} \t {lang} {len(titles)}")
        # ---
        file = t_dump_dir / f"{lang}.json"
        # ---
        dump_one(file, titles)
    # ---
    print(f"dump_data: all langs: {len(all_data)}")


def load_lang_titles(lang):
    # ---
    data = load_lang_titles_from_dump(lang)
    # ---
    if data:
        return data
    # ---
    if "local" in sys.argv:
        return {}
    # ---
    data = one_lang_titles(lang)
    # ---
    return data


def start():
    # ---
    # languages = count_all_langs()
    # ---
    all_links = langs_titles()
    # ---
    dump_data(all_links)


if __name__ == "__main__":
    start()
