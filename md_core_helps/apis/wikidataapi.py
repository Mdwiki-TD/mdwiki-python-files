#!/usr/bin/python3
"""

بوت للعمل على ويكيبيانات أو ويكيبيديا

from apis import wikidataapi
# q = wikidataapi.new_item(label="", lang="", returnid=True)

python3 core8/pwb.py apis/wikidataapi

"""

import traceback
import re
import json
import sys
import pywikibot
from datetime import datetime
import requests

# ---
from newapi import printe
from apis import user_account_new

from apis import wd_rest_new

# ---
menet = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
# ---
user_agent = user_account_new.user_agent
username = user_account_new.bot_username  # user_account_new.my_username
password = user_account_new.bot_password  # user_account_new.mdwiki_pass
# ---
if "workhimo" in sys.argv:
    username = user_account_new.my_username
    password = user_account_new.lgpass_enwiki
# ---
yes_answer = ["y", "a", "", "Y", "A", "all"]
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
timesleep = 0
wd_cach = {}
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


def post(params, apiurl="", token=True):
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
    except Exception:
        pywikibot.output("Traceback (most recent call last):")
        pywikibot.output(traceback.format_exc())
        pywikibot.output(params)
        pywikibot.output("CRITICAL:")
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
    except Exception:
        pywikibot.output("Traceback (most recent call last):")
        pywikibot.output(traceback.format_exc())
        pywikibot.output("CRITICAL:")
        return {}
    # ---
    status = get_status(r4)
    # ---
    if status != 200:
        pywikibot.output(f"<<red>> wikidataapi.py: post error status: {str(status)}")
        return {}
    # ---
    return jsone


wd_rest_new.open_url_get = open_url_get


def Get_sitelinks_From_Qid(q):
    return wd_rest_new.Get_sitelinks_From_Qid(q)


def Get_claim(q, property, get_claim_id=False):
    return wd_rest_new.Get_Claims_API(q=q, p=property)


def WD_Merge(q1, q2):
    # ---
    q11 = re.sub(r"Q", "", q1)
    q22 = re.sub(r"Q", "", q2)
    # ---
    if q11.isdigit() and q22.isdigit():
        # ---
        if int(q11) > int(q22):
            From = q1
            To = q2
        else:
            From = q2
            To = q1
    else:
        From = q2
        To = q1
    # ---
    printe.output(f"from {From} to {To} ")
    # ---
    params = {
        "action": "wbmergeitems",
        "fromid": From,
        "toid": To,
        "ignoreconflicts": "description",
        "summary": "",
    }
    # ---
    r4 = post(params, token=True)
    # ---
    if not r4:
        return False
    # ---
    if "success" in r4:
        if '"redirected":1' in r4:
            printe.output("<<green>> ** true .. redirected.")
            return True
        else:
            printe.output("<<green>> ** true.")
            # ---
            pams2 = {"action": "wbcreateredirect", "from": From, "to": To, "ignoreconflicts": "description", "summary": ""}
            # ---
            r5 = post(pams2, token=True)
            # ---
            if "success" in r5:
                printe.output("<<green>> **createredirect true.")
                return True
            else:
                printe.output(f"<<red>> r5{str(r5)}")
    else:
        printe.output(f"<<red>> r4{str(r4)}")
        return False


def Labels_API(Qid, label, lang, remove=False):
    # ---
    if not Qid:
        printe.output("Labels_API Qid == '' ")
        return False
    # ---
    if label == "" and not remove:
        printe.output("Labels_API label == '' and remove = False ")
        return False
    # ---
    # save the edit
    out = f'{Qid} label:"{lang}"@{label}.'
    # ---
    params = {
        "action": "wbsetlabel",
        "id": Qid,
        "language": lang,
        "value": label,
    }
    # ---
    req = post(params, token=True)
    # ---
    if req:
        text = str(req)
        if ("using the same description text" in text) and ("associated with language code" in text):
            # item2 = re.search(r'(Q\d+)', str(req["error"]['info'])).group(1)
            match = re.search(r"(Q\d+)", str(req["error"]["info"]))
            item2 = match.group(1) if match else "Unknown"
            printe.output(f"<<red>>API: same label item: {item2}")
        # ---
        if "success" in req:
            printe.output("<<green>> **Labels_API true.")
            return True
        else:
            printe.output(f"<<red>> r5{str(req)}")
    # ---
    return False


def get_redirects(liste):
    # ---
    redirects = {}
    # ---
    for i in range(0, len(liste), 50):
        # ---
        # group = dict(list(liste.items())[i:i+50])
        group = liste[i : i + 50]
        params = {
            "action": "query",
            "format": "json",
            "titles": "|".join(group),
            "redirects": 1,
            "utf8": 1,
        }
        # ---
        json1 = post(params, token=True)
        # ---
        if json1:
            redd = json1.get("query", {}).get("redirects", [])
            for red in redd:
                redirects[red["from"]] = red["to"]
    return redirects


def new_item(label="", lang="", summary="", returnid=False):
    # ---
    data = {"labels": {lang: {"language": lang, "value": label}}}
    # ---
    params = {
        "action": "wbeditentity",
        "new": "item",
        "summary": summary,
        "data": json.JSONEncoder().encode(data),
        "format": "json",
    }
    # ---
    req = post(params, token=True)
    # ---
    if not req:
        printe.output(f"req:str({req})")
        return False
    # ---
    if "success" not in req:
        printe.output(f"<<red>> req{str(req)}")
        return False
    # ---
    printe.output("<<green>> **Claim_API true.")
    # ---
    if returnid:
        # ---
        Qid = False
        # ---
        if "entity" in req and "id" in req["entity"]:
            Qid = req["entity"]["id"]
            printe.output(f'<<green>> new_item returnid:"{Qid}" ')
        # ---
        return Qid
    # ---
    return True


def Claim_API_str(qid, property, string):
    # ---
    printe.output(f"<<yellow>> Claim_API_str: add claim to qid: {qid}, [{property}:{string}]")
    # ---
    if string == "" or qid == "" or property == "":
        return ""
    # ---
    params = {"action": "wbcreateclaim", "entity": qid, "snaktype": "value", "property": property, "value": json.JSONEncoder().encode(string)}
    # ---
    req = post(params, token=True)
    # ---
    if not req:
        printe.output(f"req:str({req})")
        return False
    # ---
    if "success" in req:
        printe.output("<<green>> **Claim_API true.")
        return True
    else:
        printe.output(f"<<red>> req{str(req)}")
    # ---
    return False


def Delete_claim(claimid):
    # ---
    params = {"action": "wbremoveclaims", "claim": claimid}
    # ---
    req = post(params, token=True)
    # ---
    if not req:
        printe.output(f"req:str({req})")
        return False
    # ---
    if "success" in req:
        printe.output("<<green>> **Claim_API true.")
        return True
    else:
        printe.output(f"<<red>> req{str(req)}")
    # ---
    return False


def wbsearchentities(search, language):
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "search": search,
        "language": language,
        "strictlanguage": 1,
        "type": "item",
        "utf8": 1,
    }
    # ---
    req = post(params)
    # ---
    if not req:
        printe.output(" wbsearchentities no req ")
        return False
    # ---
    if "success" not in req:
        printe.output(f"<<red>> wbsearchentities: {str(req)}")
        return False
    # ---
    table = {}
    # ---
    if "search" in req:
        search = req["search"]  # list
        for s in search:
            ss = {
                "id": "Q111587429",
                "title": "Q111587429",
                "pageid": 106531075,
                "display": {"label": {"value": "User:Mr. Ibrahem/Sodium nitrite (medical use)", "language": "en"}},
                "repository": "wikidata",
                "url": "//www.wikidata.org/wiki/Q111587429",
                "concepturi": "http://www.wikidata.org/entity/Q111587429",
                "label": "User:Mr. Ibrahem/Sodium nitrite (medical use)",
                "match": {"type": "label", "language": "en", "text": "User:Mr. Ibrahem/Sodium nitrite (medical use)"},
            }
            # ---
            id = s["id"]
            table[id] = {}
            # ---
            if s.get("display", {}).get("label", {}).get("value", "") != "":
                table[id]["label"] = s["display"]["label"]["value"]
                table[id]["lang"] = s["display"]["label"]["language"]
            elif s.get("match", {}).get("type", "") == "label":
                table[id]["label"] = s["match"]["text"]
                table[id]["lang"] = s["match"]["language"]
            else:
                table[id] = s
    # ---
    return table


if __name__ == "__main__":
    qids = [
        "Q26981430"
    ]
    # ---
    for q in qids:
        printe.output(f"<<blue>>_______\n{q} :")
        # ---
        j = wd_rest_new.Get_Claims_API(q=q, p="P11143")
        # ---
        printe.output(json.dumps(j, indent=4))
