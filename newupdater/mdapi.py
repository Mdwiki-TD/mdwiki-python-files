#!/usr/bin/python3
"""

"""
import sys
import requests
# ---
import user_account_new

username = user_account_new.my_username
password = user_account_new.mdwiki_pass
user_agent = user_account_new.user_agent

session = {}
session[1] = requests.Session()
# ---
session["url"] = "https://mdwiki.org/w/api.php"
session["family"] = "mdwiki"


def print_s(s):
    if 'from_toolforge' not in sys.argv:
        print(s)


def debug_print(s):
    print(s, "</br>")


def login(lang=""):
    # ---
    if not lang:
        lang = "www"
    # ---
    api_urle = "https://www.mdwiki.org/w/api.php"
    # ---
    session[1] = requests.Session()
    # ---
    # if api_urle != session["url"]: print_s( "himoBOT3.py: login to %s. user:%s" % (api_urle , username)  )
    # ---
    family = "mdwiki"
    # ---
    session["url"] = api_urle
    session["family"] = family
    session["lang"] = lang
    # ---
    # get login token
    try:
        r1 = session[1].get(
            api_urle,
            params={
                "format": "json",
                "action": "query",
                "meta": "tokens",
                "type": "login",
            },
            timeout=10,
            headers={"User-Agent": user_agent},
        )
        r1.raise_for_status()
    except Exception as e:
        debug_print(f"login to {lang}.{family}.org Error {e}")
        return False
    # ---
    try:
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
            headers={"User-Agent": user_agent},
        )
    except Exception as e:
        debug_print(f"login to {lang}.{family}.org Error {e}")
        return False
    # ---
    print_s(r2)
    # ---
    if r2.json()["login"]["result"] != "Success":
        print_s(r2.json()["login"]["reason"])
        # raise RuntimeError(r2.json()['login']['reason'])
        return False
    else:
        print_s(f"wpref.py login Success to {lang}.{family}.org")
    # ---
    # if r2.json()['login']['result'] != 'Success': debug_print(r2.json()['login']['reason'])
    # raise RuntimeError(r2.json()['login']['reason'])
    # get edit token
    try:
        r3 = session[1].get(
            api_urle,
            params={
                "format": "json",
                "action": "query",
                "meta": "tokens",
            },
            timeout=10,
            headers={"User-Agent": user_agent},
        )
    except Exception as e:
        debug_print(f"login to {lang}.{family}.org Error {e}")
        return False
    # ---
    token = r3.json()["query"]["tokens"]["csrftoken"]
    # ---
    session["token"] = token


def submitAPI(params, Type="post", add_token=False):
    # ---
    login()
    # ---
    json1 = {}
    # ---
    if add_token or ("token" in params and params["token"] == ""):
        params["token"] = session["token"]
    # ---
    try:
        method = "POST"  # if Type == "post" else "GET"
        # ---
        r4 = session[1].request(method, session["url"], data=params, headers={"User-Agent": user_agent}, timeout=10)
        json1 = r4.json()
        # ---
    except Exception as e:
        debug_print(f"submitAPI Error {e}")
        debug_print(params)
        return json1
    # ---
    return json1


def get_revisions(title, lang=""):
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": title,
        "formatversion": "2",
        "rvprop": "comment|user|timestamp",
        "rvdir": "newer",
        "rvlimit": "max",
    }
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
        json1 = submitAPI(params, Type="post")
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
    json1 = submitAPI(params, Type="post")
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
    _err = json1.get("error", {}).get("code", {})
    # {'error': {'code': 'missingtitle', 'info': "The page you specified doesn't exist.", '*': 'See https://fr.wikipedia.org/w/api.php for API usag Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/postorius/lists/mediawiki-api-announce.lists.wikimed.org/&gt; for notice of API deprecations and breaking changes.'}, 'servedby': 'mw1362'}
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
    if not login(lang):
        return {}
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
    json1 = submitAPI(pparams, add_token=True)
    # ---
    if not json1:
        return ""
    # ---
    if "Success" in str(json1):
        print_s(f"<<green>> ** true .. [[{session['lang']}:{session['family']}:{title}]]")
        return True
    # ---
    else:
        print_s(json1)
    # ---
    return False


if __name__ == "__main__":
    login()
