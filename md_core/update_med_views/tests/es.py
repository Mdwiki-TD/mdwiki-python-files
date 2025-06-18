#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/tests/es

"""

from update_med_views.views import load_one_lang_views
from update_med_views.bot import get_one_lang_views
from update_med_views.helps import load_lang_titles_from_dump

titles = load_lang_titles_from_dump("es")
zz = get_one_lang_views("es", titles, 2023)
# ---
print(zz)
print(f"{len(zz)=:,}")
