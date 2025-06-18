#!/usr/bin/python3
"""
# ---
from mdpy.bots import make_title_bot
# _title1_ = make_title_bot.make_title(url)
# ---
"""
import re
import requests
import urllib.parse
from newapi import printe
from newapi.except_err import exception_err  # exception_err(e)

# ---
Title_cash = {}
# ---
globalbadtitles = r"""
# is
(test|
# starts with
    ^\W*(
            register
            |registration
            |(sign|log)[ \-]?in
            |subscribe
            |sign[ \-]?up
            |log[ \-]?on
            |untitled[ ]?(document|page|\d+|$)
            |404[ ]
        ).*
# anywhere
    |.*(
            403[ ]forbidden
            |(404|page|file|information|resource).*not([ ]*be)?[ ]*(available|found)
            |site.*disabled
            |error[ ]404
            |error.+not[ ]found
            |not[ ]found.+error
            |404[ ]error
            |\D404\D
            |check[ ]browser[ ]settings
            |log[ \-]?(on|in)[ ]to
            |site[ ]redirection
     ).*
# ends with
    |.*(
            register
            |access denied
            |registration
            |(sign|log)[ \-]?in
            |subscribe|sign[ \-]?up
            |log[ \-]?on
        )\W*$
)
"""


def get_url(url):
    # ---
    json1 = {}
    # ---
    try:
        req = requests.get(url, timeout=10)
        # ---
        if 500 <= req.status_code < 600:
            printe.output(f"received {req.status_code} status from {req.url}")
        else:
            json1 = req.json()
    # ---
    except Exception as e:
        exception_err(e)
    # ---
    return json1


def make_title(url):
    url = url.strip()
    url2 = ""
    # ---
    if url in Title_cash:
        return Title_cash[url]
    # ---
    Title_cash[url] = ""
    # ---
    if not url.strip():
        printe.output("<<red>> make_title url = '' return False")
        return {}
    # ---
    url2 = urllib.parse.quote(url)
    # ---
    url2 = url2.replace("/", "%2F")
    url2 = url2.replace(":", "%3A")
    url2 = url2.replace("&", "%26")
    url2 = url2.replace("#", "%23")
    # ---
    urlr = f"https://en.wikipedia.org/api/rest_v1/data/citation/mediawiki-basefields/{url2}"
    # ---
    _json1_ = [{"key": "JSJVMKE6", "version": 0, "itemType": "webpage", "creators": [], "tags": [], "title": "NCATS Inxight: Drugs — OXITRIPTAN", "url": "https://drugs.ncats.io/drug/C1LJO185Q9", "abstractNote": "Chemical", "language": "en", "accessDate": "2019-12-02", "shortTitle": "NCATS Inxight", "websiteTitle": "drugs.ncats.io"}]
    # ---
    json1 = get_url(urlr)
    # ---
    if not json1:
        return ""
    # ---
    results = json1
    # ---
    if isinstance(json1, list):
        results = json1[0]
    # ---
    title = results.get("title", "")
    # ---
    if title == "" or title.strip().lower() == "not found.":
        return ""
    # ---
    titleBlackList = re.compile(globalbadtitles, re.I | re.S | re.X)
    # ---
    if titleBlackList.match(title):
        printe.output(f"<<red>> WARNING<<default>> {url} : " "Blacklisted title ({title})")
    # ---
    Title_cash[url] = title
    # ---
    if title != "":
        printe.output(f"<<green>> make_title_bot: newtitle: ({title})")
    # ---
    return title


# ---
