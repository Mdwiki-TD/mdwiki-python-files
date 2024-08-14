#!/usr/bin/python3
"""

from apis.wd_bots.wikidataapi_post import Log_to_wiki, post_it, open_url_get

"""
import traceback
import sys
from newapi.except_err import exception_err
import pywikibot
import requests
# ---
from newapi import printe
from apis import user_account_new

user_agent = user_account_new.user_agent
username = user_account_new.bot_username  # user_account_new.my_username
password = user_account_new.bot_password  # user_account_new.mdwiki_pass
# ---
if "workhimo" in sys.argv:
    username = user_account_new.my_username
    password = user_account_new.lgpass_enwiki
# ---
r1_params = {
    "format": "json",
    "action": "query",
    "meta": "tokens",
    "type": "login",
}
r2_params = {
    # fz'assert': 'user',
    "format": "json",
    "action": "login",
    "lgname": username,
    "lgpassword": password,
}
SS = {"ss": requests.Session()}
# ---
login_not_done = {1: True}


def Log_to_wiki(url=""):
    # ---
    if not url:
        url = "https://www.wikidata.org/w/api.php"
    # ---
    if not login_not_done[1]:
        return ""
    # ---
    printe.output(f"wikidataapi.py: log to {url} user:{r2_params['lgname']}")
    SS["url"] = url
    SS["ss"] = requests.Session()
    # ---
    if SS:
        # try:
        r11 = SS["ss"].get(SS["url"], params=r1_params, headers={"User-Agent": user_agent}, timeout=10)
        r11.raise_for_status()
        # except:
        # printe.output( "wikidataapi.py: Can't log in . ")
        # log in
        r2_params["lgtoken"] = r11.json()["query"]["tokens"]["logintoken"]
        r22 = SS["ss"].post(SS["url"], data=r2_params, headers={"User-Agent": user_agent}, timeout=10)
    # except:
    else:
        printe.output("wikidataapi.py: Can't log in . ")
        return False
    # ---
    if r22.json().get("login", {}).get("result", "") != "Success":
        printe.output(r22.json()["login"]["reason"])
        # raise RuntimeError(r22.json()['login']['reason'])
    else:
        printe.output("wikidataapi.py login Success")
    # ---
    # get edit token
    SS["r33"] = SS["ss"].get(
        SS["url"],
        params={
            "format": "json",
            "action": "query",
            "meta": "tokens",
        },
        headers={"User-Agent": user_agent},
        timeout=10,
    )
    # ---
    SS["url"] = url
    # ---
    SS["r3_token"] = SS["r33"].json()["query"]["tokens"]["csrftoken"]
    # ---
    # printe.output( ' r3_token:%s' % SS["r3_token"] )
    # ---
    login_not_done[1] = False


def get_status(req):
    try:
        return req.status_code
    except BaseException:
        return req.status


def post_it(params, apiurl="", token=True):
    # ---
    if not apiurl:
        apiurl = "https://www.wikidata.org/w/api.php"
    # ---
    Log_to_wiki(url=apiurl)
    # ---
    # r4 = SS["ss"].post(SS["url"], data = params, headers={"User-Agent": user_agent}, timeout=10)
    # post to API without error handling
    # ---
    if token:
        params["token"] = SS["r3_token"]
    # ---
    params["format"] = "json"
    # ---
    jsone = {}
    # ---
    try:
        r4 = SS["ss"].request("POST", SS["url"], data=params, headers={"User-Agent": user_agent}, timeout=10)
        jsone = r4.json()
    except Exception as e:
        exception_err(e, text=params)
        return {}
    # ---
    status = get_status(r4)
    # ---
    if status != 200:
        pywikibot.output(f"<<red>> wikidataapi.py: post error status: {str(status)}")
        return {}
    # ---
    return jsone

def open_url_get(url):
    # ---
    Log_to_wiki()
    # ---
    jsone = {}
    # ---
    try:
        r4 = SS["ss"].request("GET", url, headers={"User-Agent": user_agent}, timeout=10)
        jsone = r4.json()
    except Exception as e:
        exception_err(e)
        return {}
    # ---
    status = get_status(r4)
    # ---
    if status != 200:
        pywikibot.output(f"<<red>> wikidataapi.py: post error status: {str(status)}")
        return {}
    # ---
    return jsone
