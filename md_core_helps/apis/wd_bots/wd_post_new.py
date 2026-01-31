#!/usr/bin/python3
"""

python3 core8/pwb.py apis/wd_bots/wd_post_new

from apis.wd_bots.wd_post_new import post_it

"""
import logging
import sys

from apis import user_account_new
from apis.sup.su_login import Get_MwClient_Site

logger = logging.getLogger(__name__)

user_agent = user_account_new.user_agent
username = user_account_new.bot_username  # user_account_new.my_username
password = user_account_new.bot_password  # user_account_new.mdwiki_pass

if "workhimo" in sys.argv:
    username = user_account_new.my_username
    password = user_account_new.lgpass_enwiki

SS = {"csrftoken": ""}

wd_site = Get_MwClient_Site("www", "wikidata", username, password)


def do_request(params=None, method="POST"):
    # ---
    if not wd_site:
        print("no wd_site")
        return {}
    # ---
    params = params.copy()
    # ---
    action = params["action"]
    # ---
    del params["action"]
    # ---
    try:
        r4 = wd_site.api(action, http_method=method, **params)
        return r4

    except Exception as e:
        logger.warning(e)
    # ---
    return {}


def get_token(mk_new=False):
    # get edit token
    # ---
    if SS["csrftoken"] and not mk_new:
        return SS["csrftoken"]
    # ---
    try:
        csrftoken = wd_site.get_token("csrf")
    except Exception as e:
        logger.error(f"Could not get token: {e}")
        return False
    # ---
    SS["csrftoken"] = csrftoken
    # ---
    return csrftoken


def post_it(params=None, url=None, token=True, method="POST"):
    # ---
    if not url:
        url = "https://www.wikidata.org/w/api.php"
    # ---
    if token:
        params["token"] = get_token()
    # ---
    params["format"] = "json"
    # ---
    if method not in ["POST", "GET"]:
        method = "POST"
    # ---
    jsone = do_request(params=params, method=method)
    # ---
    return jsone
