#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/tests/es -para:2 -lang:es -year:2024
python3 core8/pwb.py update_med_views/tests/es -para:2 -lang:en -year:2024 printurl

"""
import sys

from update_med_views.bot import get_one_lang_views
from update_med_views.views import load_one_lang_views
from update_med_views.helps import load_lang_titles_from_dump


def parse_args():
    year = 2024
    lang = "ar"
    # ---
    for arg in sys.argv:
        key, _, val = arg.partition(':')
        # ---
        if key in ['lang', '-lang']:
            lang = val
        # ---
        if key in ['year', '-year'] and val.isdigit():
            year = int(val)
    # ---
    return year, lang


year, lang = parse_args()

titles = load_lang_titles_from_dump(lang)
print(f"titles: {len(titles)}")

# zz = load_one_lang_views(lang, titles, year, max_items=1000)
# print(f"{len(zz)=:,}")



zz = get_one_lang_views(lang, titles, year)
# ---
print(zz)
