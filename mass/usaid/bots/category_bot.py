"""

from mass.eyerounds.bots.category_bot import create_category # create_category(album_name, pages)

"""

import sys
from nccommons import api
from newapi import printe


def create_category(cat, album_url, album_id, pages) -> str:
    cat = cat.replace("_", " ").replace("  ", " ")
    # ---
    cat_title = f"Category:{cat}"
    # ---
    cat_text = (
        f"* Album url: [{album_url} {album_id}].\n"
        "[[Category:USAID]]"
    )
    # ---
    if "nocat" in sys.argv:
        return cat_title
    # ---
    if cat_title in pages:
        printe.output(f"<<lightyellow>>{cat_title} already exists")
        return cat_title
    # ---
    api.create_Page(cat_text, cat_title)
    # ---
    return cat_title
