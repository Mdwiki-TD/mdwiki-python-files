import os
import sys
from newapi import printe

from newapi.accounts.useraccount import User_tables_bot, User_tables_ibrahem
from newapi import LoginWrap

logins_cache = {}


def log_in_wikidata(Mr_or_bot="bot"):
    # ---
    users_data = User_tables_bot if Mr_or_bot == "bot" else User_tables_ibrahem
    # ---
    login_bot, logins_cache2 = LoginWrap("www", "wikidata", logins_cache, users_data)
    # ---
    logins_cache.update(logins_cache2)
    # ---
    print(logins_cache)
    # ---
    return login_bot


bot = log_in_wikidata(Mr_or_bot="notbot")


def session_post(params):
    return bot.post_params(params, Type="get", addtoken=False, GET_CSRF=True, files=None, do_error=False, max_retry=0)
