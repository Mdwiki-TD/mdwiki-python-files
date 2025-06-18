#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/tests/views

"""
import sys

from update_med_views.bot import get_one_lang_views

titles = [
    "اليمن",
    "Atsʼiis naałdzid",
    "asdasdasxxx!!##as",
]
# ---
# zz = load_one_lang_views("nv", titles, 2023)
zz = get_one_lang_views("ar", titles, 2023)
# ---
print(zz)
