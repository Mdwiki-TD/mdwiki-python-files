#!/usr/bin/python3
"""

from apis.wd_bots.wikidataapi_post import Log_to_wiki, post_it

"""
import logging
import sys
from urllib.parse import urlencode

import requests
from apis import user_account_new

logger = logging.getLogger(__name__)

user_agent = user_account_new.user_agent
username = user_account_new.bot_username  # user_account_new.my_username
password = user_account_new.bot_password  # user_account_new.mdwiki_pass

if "workhimo" in sys.argv:
    username = user_account_new.my_username
    password = user_account_new.lgpass_enwiki

SS = {"ss": requests.Session(), "r3_token": ""}

login_not_done = {1: True}


def do_request(params=None, method="POST"):
    # ---
    url = "https://www.wikidata.org/w/api.php"
    # ---
    args = {
        "headers": {"User-Agent": user_agent},
        "timeout": 10,
    }
    # ---
    if method == "POST":
        args["data"] = params
    else:
        args["params"] = params
    # ---
    unurl = f"{url}?{urlencode(params)}"
    # ---
    if "printurl" in sys.argv:
        logger.info(f"do_request:\t\t{unurl}")
    # ---
    try:
        r4 = SS["ss"].request(method, url, **args)
        status = r4.status_code
        # ---
        if status != 200:
            logger.info(f"<<red>> wikidataapi.py: post error status: {str(status)}")
            return {}
        # ---
        return r4.json()

    except Exception as e:
        logger.warning(e)
        return {}


def get_token(mk_new=False):
    # get edit token
    # ---
    if SS["r3_token"] and not mk_new:
        return SS["r3_token"]
    # ---
    params = {"format": "json", "action": "query", "meta": "tokens"}
    # ---
    result = do_request(params=params)
    # ---
    r3_token = result.get("query", {}).get("tokens", {}).get("csrftoken")
    # ---
    SS["r3_token"] = r3_token
    # ---
    return r3_token


def Log_to_wiki(url=""):
    # ---
    if not login_not_done[1]:
        return ""
    # ---
    r1_params = {"format": "json", "action": "query", "meta": "tokens", "type": "login"}
    # ---
    r2_params = {"format": "json", "action": "login", "lgname": username, "lgpassword": password}
    # ---
    if not url:
        url = "https://www.wikidata.org/w/api.php"
    # ---
    logger.info(f"wikidataapi.py: log to {url} user:{r2_params['lgname']}")
    # ---
    SS["url"] = url
    SS["ss"] = requests.Session()
    # ---
    try:
        r11 = SS["ss"].get(SS["url"], params=r1_params, headers={"User-Agent": user_agent}, timeout=10)
        # ---
        r11.raise_for_status()
        r2_params["lgtoken"] = r11.json()["query"]["tokens"]["logintoken"]
        r22 = SS["ss"].post(SS["url"], data=r2_params, headers={"User-Agent": user_agent}, timeout=10)
    except Exception as e:
        logger.info("wikidataapi.py: Can't log in . ")
        return False
    # ---
    if r22.json().get("login", {}).get("result", "") != "Success":
        logger.info(r22.json()["login"]["reason"])
    else:
        logger.info("wikidataapi.py login Success")
    # ---
    SS["url"] = url
    # ---
    get_token(mk_new=True)
    # ---
    login_not_done[1] = False


def post_it(params=None, url=None, token=True, method="POST"):
    # ---
    Log_to_wiki()
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
