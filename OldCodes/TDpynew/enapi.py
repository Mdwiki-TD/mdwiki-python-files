#!/usr/bin/python3
"""

Usage:
from TDpynew import enapi
# result = enapi.submitAPI(params, addtoken=False)

"""

#
# (C) Ibrahem Qasim, 2022
#
#
import json
import traceback

import requests
from TDpynew import user_account_new

# ---
SS = {}
# ---
lgname_enwiki = user_account_new.lgname_enwiki
lgpass_enwiki = user_account_new.lgpass_enwiki
# ---
login_done = {1: False}
print_pywikibot = {1: False}
# ---
try:
    import pywikibot

    print_pywikibot[1] = True
except BaseException:
    print_pywikibot[1] = False


def printt(s):
    if print_pywikibot[1]:
        pywikibot.output(s)


def login():
    # ---
    SS["ss"] = requests.Session()
    SS["url"] = "https://" + "en.wikipedia.org/w/api.php"
    SS["ss"] = requests.Session()
    # ---
    r11 = SS["ss"].get(
        SS["url"],
        params={
            "format": "json",
            "action": "query",
            "meta": "tokens",
            "type": "login",
        },
    )
    r11.raise_for_status()
    # log in
    r22 = SS["ss"].post(
        SS["url"],
        data={
            # 'assert': 'user',
            "format": "json",
            "action": "login",
            "lgname": lgname_enwiki,
            "lgpassword": lgpass_enwiki,
            "lgtoken": r11.json()["query"]["tokens"]["logintoken"],
        },
    )
    # ---
    # printt( f'__file__:{__file__}' )
    # ---
    if r22.json()["login"]["result"] != "Success":
        ress = r22.json()["login"]["result"]
        if print_pywikibot[1]:
            pywikibot.output("Traceback (most recent call last):")
            pywikibot.output(f"Exception:{str(ress)}")
            pywikibot.output(traceback.format_exc())
            pywikibot.output("CRITICAL:")
    else:
        printt(f"<<lightgreen>> mdwiki/TDpynew/mdapi.py: log to {SS['url']} user:{lgname_enwiki} Success... ")
    # ---
    # get edit token
    SS["r33"] = SS["ss"].get(
        SS["url"],
        params={
            "format": "json",
            "action": "query",
            "meta": "tokens",
        },
    )
    # ---
    SS["r3_token"] = SS["r33"].json()["query"]["tokens"]["csrftoken"]
    login_done[1] = True


def submitAPI(params, addtoken=True):
    # ---
    if not login_done[1]:
        login()
    # ---
    if addtoken:
        params["token"] = SS["r3_token"]
    # ---
    json1 = {}
    # ---
    try:
        r4 = SS["ss"].post(SS["url"], data=params)
        json1 = json.loads(r4.text)
    except Exception:
        if print_pywikibot[1]:
            pywikibot.output("Traceback (most recent call last):")
            pywikibot.output(traceback.format_exc())
            pywikibot.output("CRITICAL:")
        return {}
    # ---
    return json1
