#!/usr/bin/python3
"""
from newupdater.api import login, submitAPI, GetPageText, missingtitles, page_put
"""
import json
import sys
import requests

# ---
try:
    import pywikibot
except ImportError:
    pywikibot = None
# ---
from newupdater.helps import print_s

from newupdater import user_account_new

username = user_account_new.my_username
password = user_account_new.mdwiki_pass

session = {}
session[1] = requests.Session()
session["url"] = ""
# ---
Url_To_login = {1: "", "not": True}
# ---
login_done = {1: False}
# ---
yes_answer = ["y", "a", "", "Y", "A", "all"]
# ---
ask_a = {1: False}
# ---
missingtitles = {}


def login(lang):
    # ---
    if not lang:
        lang = "www"
    # ---
    if login_done[1] == lang:
        return ""
    # ---
    api_urle = "https://www.mdwiki.org/w/api.php"
    # ---
    Url_To_login[1] = api_urle
    # ---
    session[1] = requests.Session()
    # ---
    # if api_urle != session["url"]: print_s( "himoBOT3.py: login to %s. user:%s" % (api_urle , username)  )
    # ---
    session["url"] = api_urle
    session["family"] = "mdwiki"
    session["lang"] = lang
    # ---
    # get login token
    r1 = session[1].get(
        api_urle,
        params={
            "format": "json",
            "action": "query",
            "meta": "tokens",
            "type": "login",
        },
        timeout=10,
    )
    r1.raise_for_status()
    # ---
    r2 = session[1].post(
        api_urle,
        data={
            "format": "json",
            "action": "login",
            "lgname": username,
            "lgpassword": password,
            "lgtoken": r1.json()["query"]["tokens"]["logintoken"],
        },
        timeout=10,
    )
    # ---
    print_s(r2)
    if r2.json()["login"]["result"] != "Success":
        print_s(r2.json()["login"]["reason"])
        # raise RuntimeError(r2.json()['login']['reason'])
    else:
        print_s(f"wpref.py login Success to {lang}.mdwiki.org")
        login_done[1] = lang
    # ---
    # if r2.json()['login']['result'] != 'Success': print(r2.json()['login']['reason'])
    # raise RuntimeError(r2.json()['login']['reason'])
    # get edit token
    r3 = session[1].get(
        api_urle,
        params={
            "format": "json",
            "action": "query",
            "meta": "tokens",
        },
        timeout=10,
    )
    # ---
    token = r3.json()["query"]["tokens"]["csrftoken"]
    # ---
    session["token"] = token


def Gettoken():
    return session["token"]


def submitAPI(params, lang="www", Type="post"):
    # ---
    login(lang)
    # ---
    json1 = {}
    # ---
    if "token" in params and params["token"] == "":
        params["token"] = session["token"]
    # ---
    r4_text = ""
    # ---
    try:
        if Type == "post":
            r4 = session[1].post(session["url"], data=params, timeout=10)
        else:
            r4 = session[1].get(session["url"], data=params, timeout=10)
        # ---
        r4_text = r4.text
    except Exception as e:
        print_s(f"submitAPI r4 Error {e}")
        return json1
    # ---
    if r4_text != "":
        try:
            json1 = json.loads(r4_text)
        except Exception as e:
            print_s(f"submitAPI Error {e}")
            # print_s(r4_text)
            print_s(params)
            return json1
    # ---
    return json1


def get_revisions(title, lang=""):
    params = {"action": "query", "format": "json", "prop": "revisions", "titles": title, "formatversion": "2", "rvprop": "comment|user|timestamp", "rvdir": "newer", "rvlimit": "max"}
    # ---
    rvcontinue = "x"
    # ---
    revisions = []
    # ---
    while rvcontinue != "":
        # ---
        if rvcontinue != "x":
            params["rvcontinue"] = rvcontinue
        # ---
        json1 = submitAPI(params, lang=lang)
        # ---
        if not json1 or not isinstance(json1, dict):
            return ""
        # ---
        rvcontinue = json1.get("continue", {}).get("rvcontinue", "")
        # ---
        pages = json1.get("query", {}).get("pages", [{}])
        # ---
        for p in pages:
            _revisions = p.get("revisions", [])
            revisions.extend(_revisions)
    # ---
    return revisions


def GetPageText2(title):
    # ---
    url = "https://mdwiki.org/wiki/" + title + "?action=raw"
    # ---
    try:
        r = requests.get(url, timeout=5)
        # r.raise_for_status()
        return r.text
    except Exception as e:
        print_s(f"GetPageText2 Error {e}")
        return ""


def GetPageText(title, lang="", Print=True):
    # ---
    params = {
        "action": "parse",
        "format": "json",
        # "prop": "wikitext|sections",
        "prop": "wikitext",
        "page": title,
        # "redirects": 1,
        "utf8": 1,
        # "normalize": 1,
    }
    # ---
    json1 = submitAPI(params, lang=lang)
    # ---
    if not json1 or not isinstance(json1, dict):
        if Print:
            print_s("json1 ==:")
            print_s(json1)
        return ""
    # ---
    if not json1:
        if Print:
            print_s("json1 == {}")
        return ""
    # ---
    err = json1.get("error", {}).get("code", {})
    # {'error': {'code': 'missingtitle', 'info': "The page you specified doesn't exist.", '*': 'See https://fr.wikipedia.org/w/api.php for API usag Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/postorius/lists/mediawiki-api-announce.lists.wikimed.org/&gt; for notice of API deprecations and breaking changes.'}, 'servedby': 'mw1362'}
    # ---
    if err == "missingtitle":
        missingtitles[title] = lang
    # ---
    parse = json1.get("parse", {})
    if not parse:
        if Print:
            print_s("parse == {}")
            print_s(json1)
        return ""
    # ---
    text = parse.get("wikitext", {}).get("*", "")
    # ---
    if not text:
        if Print:
            print_s(f'page {title} text == "".')
    # ---
    return text


def page_put(oldtext, NewText, summary, title, lang):
    # ---
    if "ask" in sys.argv and not ask_a[1]:
        # ---
        if pywikibot:
            pywikibot.showDiff(oldtext, NewText)
        # ---
        print_s(f" -Edit summary: {summary}:")
        sa = input(f"<<lightyellow>>mdwiki/wpref.py: Do you want to accept these changes? ([y]es, [N]o, [a]ll): for page ({lang}:{title})")
        # ---
        if sa == "a" or sa == "all":
            ask_a[1] = True
            print_s(" <<lightgreen>>mdwiki/wpref.py: All changes accepted.")
            print_s(" <<lightgreen>>mdwiki/wpref.py: All changes accepted.")
        # ---
        if sa not in yes_answer:
            print_s("wrong answer")
            return False
    # ---
    pparams = {
        "action": "edit",
        "format": "json",
        # "maxlag": ar_lag[1],
        "title": title,
        "text": NewText,
        "summary": summary,
        # "starttimestamp": starttimestamp,
        # "minor": minor,
        # "notminor": 1,
        "bot": 1,
        "nocreate": 1,
        "token": session["token"],
    }
    # ---
    r4 = session[1].post(session["url"], data=pparams)
    # ---
    if "Success" in r4.text:
        print_s(f"<<lightgreen>> ** true .. [[{session['lang']}:{session['family']}:{title}]]")
        return True
    # ---
    else:
        print_s(r4.text)
    # ---
    return False