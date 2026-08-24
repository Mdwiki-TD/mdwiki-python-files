# ---
"""
'''
"""

import functools
import os
import sys

if "mwclient" not in sys.argv:
    sys.argv.append("nomwclient")

from newapi import AllAPIS

my_username = os.getenv("WIKIPEDIA_HIMO_USERNAME") or ""
mdwiki_pass = os.getenv("MDWIKI_HIMO_PASSWORD") or ""


@functools.lru_cache(maxsize=1)
def load_main_api() -> AllAPIS:
    username = os.getenv("WIKIPEDIA_HIMO_USERNAME") or ""
    password = os.getenv("MDWIKI_HIMO_PASSWORD") or ""

    if not username or not password:
        raise RuntimeError("Missing credentials: WIKIPEDIA_HIMO_USERNAME / MDWIKI_HIMO_PASSWORD")

    return AllAPIS(
        lang="www",
        family="mdwiki",
        username=username,
        password=password,
        use_cookies=False,
    )


main_api = load_main_api()

NewApi = main_api.newapi
MainPage = main_api.mainpage
CatDepth = main_api.catdepth
md_MainPage = MainPage  # noqa: N816

__all__ = [
    "MainPage",
    "md_MainPage",
    "NewApi",
    "CatDepth",
]
