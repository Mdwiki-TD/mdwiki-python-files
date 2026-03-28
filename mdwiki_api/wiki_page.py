"""

"""

import functools
import logging
import os
from newapi import ALL_APIS

from dotenv import load_dotenv
try:
    load_dotenv()
except Exception:
    pass

user_agent = "WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"
username = os.getenv("WIKIPEDIA_BOT_USERNAME")
password = os.getenv("WIKIPEDIA_BOT_PASSWORD")

logger = logging.getLogger(__name__)

logger.info(f"wiki_page.py use {username} account.")

change_codes = {
    "bat_smg": "bat-smg",
    "be-x-old": "be-tarask",
    "be_x_old": "be-tarask",
    "cbk_zam": "cbk-zam",
    "fiu_vro": "fiu-vro",
    "map_bms": "map-bms",
    "nb": "no",
    "nds_nl": "nds-nl",
    "roa_rup": "roa-rup",
    "zh_classical": "zh-classical",
    "zh_min_nan": "zh-min-nan",
    "zh_yue": "zh-yue",
}


@functools.lru_cache(maxsize=1024)
def load_main_api(lang="www", family="wikipedia") -> ALL_APIS:
    return ALL_APIS(
        lang=lang,
        family=family,
        username=username,
        password=password,
    )


def MainPage(title, lang, family="wikipedia"):
    main_api = load_main_api(lang, family)
    return main_api.MainPage(title)


def CatDepth(title, sitecode="", family="wikipedia", **kwargs) -> dict:
    main_api = load_main_api(sitecode, family)
    return main_api.CatDepth(title, sitecode=sitecode, family=family, **kwargs)


def NEW_API(lang="", family="wikipedia"):
    main_api = load_main_api(lang, family)
    return main_api.NEW_API()


__all__ = [
    "user_agent",
    "MainPage",
    "NEW_API",
    "CatDepth",
    "change_codes",
]
