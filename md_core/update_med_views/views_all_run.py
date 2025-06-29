#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/views_all_run

tfj run views0 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py update_med_views/views_all_run start"
tfj run views --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py update_med_views/views_all_run start -max:1000"
tfj run views1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py update_med_views/views_all_run start -min:1000 -max:5000"
tfj run views2 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py update_med_views/views_all_run start -min:5000 -max:10000"
tfj run views3 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py update_med_views/views_all_run start -min:10000 -max:19000"
tfj run views4 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py update_med_views/views_all_run start -min:19000"

"""
import sys
from newapi import printe
from update_med_views.helps import load_lang_titles_from_dump
from update_med_views.helps import load_languages_counts
from update_med_views.views_all import load_one_lang_views_all, article_all_views


def start():
    # python3 core8/pwb.py update_med_views/views_all_run start
    langs = load_languages_counts()
    # ---
    maxv = 1000000
    minx = 0
    # ---
    for arg in sys.argv:
        key, _, val = arg.partition(':')
        if key in '-max' and val.isdigit():
            maxv = int(val)
        elif key in '-min' and val.isdigit():
            minx = int(val)
    # ---
    # sort langs by len of titles { "ar": 19972, "bg": 2138, .. }
    langs = dict(sorted(langs.items(), key=lambda item: item[1], reverse=False))
    # ---
    to_work = {}
    # ---
    for lang, _ in langs.items():
        titles = load_lang_titles_from_dump(lang)
        # ---
        if len(titles) == 0:
            continue
        # ---
        if minx > 0 and len(titles) < minx:
            printe.output(f"<<yellow>> {lang}>> len titles ({len(titles)}) < min {minx}, skipping")
            continue
        # ---
        if len(titles) > maxv:
            printe.output(f"<<yellow>> {lang}>> len titles ({len(titles)}) > max {maxv}, skipping")
            continue
        # ---
        to_work[lang] = titles
    # ---
    printe.output(f"<<green>> to_work: {len(to_work)}")
    # ---
    for lang, titles in to_work.items():
        # ---
        printe.output(f"<<yellow>>lang:{lang},\ttitles: {len(titles)}")
        # ---
        if "no" not in sys.argv:
            load_one_lang_views_all(lang, titles, "all")


def test2():
    # python3 core8/pwb.py update_med_views/views_all_run test2
    titles = ["Yemen", "COVID-19", "Iran–Israel war", "wj2340-0"]
    # ---
    ux = article_all_views('en', titles, 2024)
    # ---
    for t, tt in ux.items():
        print(t, tt)
    # ---
    print(f"{len(ux)=:,}")


def test(lang="pa"):
    # python3 core8/pwb.py update_med_views/views_all_run test
    titles = load_lang_titles_from_dump(lang)
    load_one_lang_views_all(lang, titles, "all")


if __name__ == '__main__':
    # ---
    defs = {
        "start": start,
        "test2": test2,
        "test": test,
    }
    # ---
    lang = ""
    # ---
    for arg in sys.argv:
        key, _, val = arg.partition(':')
        if key == '-lang':
            lang = val
        # ---
        if arg in defs:
            defs[arg]()
    # ---
    # python3 core8/pwb.py update_med_views/views_all_run -lang:ha
    # python3 core8/pwb.py update_med_views/views_all_run -lang:kn
    if len(lang) > 0:
        test(lang)
