"""

from copy_to_en.tf_page import get_cx, get_md
# CatDepth, MainPage = get_cx()
# CatDepth, MainPage = get_md()

"""

from copy_to_en.bots import medwiki_account
from newapi import ALL_APIS


def get_cx():
    # ---
    api = ALL_APIS(
        lang="mdwikicx",
        family="toolforge",
        username=medwiki_account.username_cx,
        password=medwiki_account.password_cx,
    )
    # ---
    CatDepth = api.CatDepth
    MainPage = api.MainPage
    # ---
    return CatDepth, MainPage


def get_md():
    # ---
    api = ALL_APIS(
        lang="medwiki",
        family="toolforge",
        username=medwiki_account.username,
        password=medwiki_account.password,
    )
    # ---
    CatDepth = api.CatDepth
    MainPage = api.MainPage
    # ---
    return CatDepth, MainPage
