""" """

import functools
import logging
import os
from typing import Any

from dotenv import load_dotenv

from newapi import AllAPIS
from newapi.client_wiki import bot_api

logger = logging.getLogger(__name__)

try:
    load_dotenv()
except Exception:
    pass

user_agent = "WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"
username = os.getenv("WIKIPEDIA_BOT_USERNAME") or ""
password = os.getenv("WIKIPEDIA_BOT_PASSWORD") or ""

logger.info(f"wiki_page.py use {username} account.")


@functools.lru_cache(maxsize=1024)
def load_main_api(lang: str = "www", family: str = "wikipedia") -> AllAPIS:
    return AllAPIS(
        lang=lang,
        family=family,
        username=username,
        password=password,
    )


def mainpage(title: str, lang: str, family: str = "wikipedia"):
    main_api = load_main_api(lang, family)
    return main_api.mainpage(title)


def catdepth(
    title: str,
    sitecode: str = "",
    family: str = "wikipedia",
    **kwargs,
) -> dict[str, Any]:
    sitecode = sitecode or "www"
    main_api = load_main_api(sitecode, family)
    return main_api.catdepth(
        title,
        sitecode=sitecode,
        family=family,
        **kwargs,
    )


def newapi(lang: str = "", family: str = "wikipedia") -> bot_api.NewApi:
    lang = lang or "www"
    main_api = load_main_api(lang, family)
    return main_api.newapi()


__all__ = [
    "user_agent",
    "mainpage",
    "newapi",
    "catdepth",
]
