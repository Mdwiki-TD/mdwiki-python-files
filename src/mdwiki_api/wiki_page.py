""" """

import functools
import logging
import os

from dotenv import load_dotenv

from newapi import AllAPIS

try:
    load_dotenv()
except Exception:
    pass

user_agent = "WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"
username = os.getenv("WIKIPEDIA_BOT_USERNAME")
password = os.getenv("WIKIPEDIA_BOT_PASSWORD")

logger = logging.getLogger(__name__)

logger.info(f"wiki_page.py use {username} account.")


@functools.lru_cache(maxsize=1024)
def load_main_api(lang: str = "www", family: str = "wikipedia") -> AllAPIS:
    return AllAPIS(
        lang=lang,
        family=family,
        username=username,
        password=password,
    )


def MainPage(title, lang, family: str = "wikipedia"):
    main_api = load_main_api(lang, family)
    return main_api.MainPage(title)


def CatDepth(
    title,
    sitecode: str = "",
    family: str = "wikipedia",
    **kwargs,
) -> dict:
    sitecode = sitecode or "www"
    main_api = load_main_api(sitecode, family)
    return main_api.CatDepth(
        title,
        sitecode=sitecode,
        family=family,
        **kwargs,
    )


def NewApi(lang: str = "", family: str = "wikipedia"):
    lang = lang or "www"
    main_api = load_main_api(lang, family)
    return main_api.NewApi()


__all__ = [
    "user_agent",
    "MainPage",
    "NewApi",
    "CatDepth",
]
