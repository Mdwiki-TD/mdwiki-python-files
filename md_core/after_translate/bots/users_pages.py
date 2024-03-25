#!/usr/bin/python3
"""

Usage:
from after_translate.bots.users_pages import not_pages

"""

# ---

# ---
from newapi import printe


def not_pages(lista):
    # ---
    printe.output("<<green>> start bot users_pages:")
    # ---
    tab = {}
    # ---
    for ta in lista:
        lang = ta["lang"]
        # ---
        if lang not in tab:
            tab[lang] = []
        # ---
        tab[lang].append(ta)
    # ---
    for lang, tabs in tab.items():
        # ---
        printe.output(f"<<blue>> {lang=}, pages: {len(tabs)}:")
        # ---
        for ta in tabs:
            mdtitle = ta["mdtitle"]
            target = ta["target"]
            user = ta["user"]
            pupdate = ta["pupdate"]
            namespace = ta["namespace"]
            # ---
            printe.output(f"{target=}, {user=}, {mdtitle=}, {pupdate=}, {namespace=}")
            # ---
