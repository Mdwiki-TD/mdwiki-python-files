"""

from nc_import.api_bots.wiki_page import ncc_MainPage, ncc_NEW_API

"""
import sys
from newapi.super import super_login
from newapi.super import bot_api
from newapi.super import super_page
from newapi.super import catdepth_new
from mdpy.bots import user_account_new

# ---
# User_tables = {"username": user_account_new.my_username, "password": user_account_new.my_password}
# ---
# if "botuser" in sys.argv:
User_tables = {"username": user_account_new.bot_username, "password": user_account_new.bot_password}
# ---
super_login.User_tables["wikipedia"] = User_tables
# ---
Login = super_login.Login
# ---
bot_api.login_def = Login
super_page.login_def = Login
catdepth_new.login_def = Login
# ---
NEW_API = bot_api.NEW_API
MainPage = super_page.MainPage
change_codes = super_page.change_codes
CatDepth = catdepth_new.subcatquery
CatDepthLogin = catdepth_new.login_wiki
# ---
# xxxxxxxxxxx


def test():
    page = MainPage("Mr. Ibrahem/sandbox", "ar", family="wikipedia")
    exists = page.exists()
    text = page.get_text()
    timestamp = page.get_timestamp()
    user = page.get_user()
    links = page.page_links()
    words = page.get_words()
    purge = page.purge()
    templates = page.get_templates()
    save_page = page.save(newtext="", summary="", nocreate=1, minor="")


if __name__ == "__main__":
    # python3 core8/pwb.py nc_import/api_bots/wiki_page ask
    super_page.print_test[1] = True
    super_login.print_test[1] = True
    test()
