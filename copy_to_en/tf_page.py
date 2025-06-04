"""

from copy_to_en.tf_page import get_cx, get_md
# CatDepth, MainPage = get_cx()
# CatDepth, MainPage = get_md()

"""
from copy_to_en.bots import medwiki_account
# ---
def get_cx():
    # ---
    from newapi import toolforge_page as toolforge_page_cx
    # ---
    User_tables_cx = {
        "username": medwiki_account.username_cx,
        "password": medwiki_account.password_cx,
    }
    # ---
    toolforge_page_cx.add_Usertables(User_tables_cx, "toolforge", "mdwikicx")
    # ---
    CatDepth = toolforge_page_cx.CatDepth
    MainPage = toolforge_page_cx.MainPage
    # ---
    return CatDepth, MainPage

def get_md():
    # ---
    from newapi import toolforge_page as toolforge_page_md
    # ---
    User_tables_md = {
        "username": medwiki_account.username,
        "password": medwiki_account.password,
    }
    # ---
    toolforge_page_md.add_Usertables(User_tables_md, "toolforge", "medwiki")
    # ---
    CatDepth = toolforge_page_md.CatDepth
    MainPage = toolforge_page_md.MainPage
    # ---
    return CatDepth, MainPage
