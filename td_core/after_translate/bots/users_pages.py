#!/usr/bin/python3
"""

Usage:
from after_translate.bots.users_pages import not_pages

"""

import logging

logger = logging.getLogger(__name__)


def not_pages(lista):
    # ---
    logger.info("<<green>> start bot users_pages:")
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
        logger.info(f"<<blue>> {lang=}, pages: {len(tabs)}:")
        # ---
        for ta in tabs:
            mdtitle = ta["mdtitle"]
            target = ta["target"]
            user = ta["user"]
            pupdate = ta["pupdate"]
            namespace = ta["namespace"]
            # ---
            logger.info(f"{target=}, {user=}, {mdtitle=}, {pupdate=}, {namespace=}")
            # ---
