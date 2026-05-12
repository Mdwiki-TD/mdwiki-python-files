"""

from copy_to_en.tf_page import get_cx, get_md
# CatDepth, MainPage = get_cx()
# CatDepth, MainPage = get_md()

"""

import os

from newapi import AllAPIS


def get_cx():
    # ---
    username_cx: str = os.getenv("MDWIKI_CX_USERNAME")
    password_cx: str = os.getenv("MDWIKI_CX_PASSWORD")
    # ---
    api = AllAPIS(
        lang="mdwikicx",
        family="toolforge",
        username=username_cx,
        password=password_cx,
    )
    # ---
    CatDepth = api.CatDepth
    MainPage = api.MainPage
    # ---
    return CatDepth, MainPage


def get_md():
    # ---
    username: str = os.getenv("MDWIKI_USERNAME")
    password: str = os.getenv("MDWIKI_PASSWORD")
    # ---
    api = AllAPIS(
        lang="medwiki",
        family="toolforge",
        username=username,
        password=password,
    )
    # ---
    CatDepth = api.CatDepth
    MainPage = api.MainPage
    # ---
    return CatDepth, MainPage
