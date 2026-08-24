""" """

import functools
import os
from typing import Any

from .client_wiki import bot_api
from .client_wiki.all_apis import AllAPIS
from .config import main_settings


@functools.lru_cache(maxsize=1)
def _load_credentials() -> tuple[str, str]:
    username = os.getenv("WIKIPEDIA_BOT_USERNAME", "")
    password = os.getenv("WIKIPEDIA_BOT_PASSWORD", "")

    if main_settings.bot.workibrahem:
        username = os.getenv("WIKIPEDIA_HIMO_USERNAME", "")
        password = os.getenv("WIKIPEDIA_HIMO_PASSWORD", "")

    return username, password


@functools.lru_cache(maxsize=1024)
def load_main_api(lang: str, family: str = "wikipedia") -> AllAPIS:
    """
    Loads and returns an instance of AllAPIS for the specified language and family, using cached credentials.
    """
    username, password = _load_credentials()
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
    main_api = load_main_api(sitecode, family)
    return main_api.catdepth(
        title,
        sitecode=sitecode,
        family=family,
        **kwargs,
    )


def newapi(lang: str = "", family: str = "wikipedia") -> bot_api.NewApi:
    main_api = load_main_api(lang, family)
    return main_api.newapi()


__all__ = [
    "mainpage",
    "newapi",
    "catdepth",
]
