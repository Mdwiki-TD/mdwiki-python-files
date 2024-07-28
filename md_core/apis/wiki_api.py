#!/usr/bin/python3
"""
# ---
from apis import wiki_api
# wiki_api.submitAPI( params, site="en", returnjson = False )
# ---
"""
from newapi.wiki_page import NEW_API

api_news = {}


def submitAPI(params, site="", returnjson=False):
    # ---
    params["format"] = "json"
    # ---
    if site not in api_news:
        api_news[site] = NEW_API(site, family="wikipedia")
    # ---
    json1 = api_news[site].api_new.post_params(params, addtoken=True)
    # ---
    return json1


def Get_page_qid(sitecode, title):
    # ---
    if sitecode.endswith("wiki"):
        sitecode = sitecode[:-4]
    # ---
    params = {
        "action": "query",
        "format": "json",
        # "prop": "langlinks|pageprops",
        "titles": title,
        "redirects": 1,
        "prop": "pageprops",
        "ppprop": "wikibase_item",
        "utf8": 1,
    }
    # ---
    json1 = submitAPI(params, site=sitecode)
    # ---
    if not json1:
        return ""
    # ---
    js_query = json1.get("query", {})
    # ---
    pages = js_query.get("pages", {})
    # ---
    qid = ""
    # ---
    for id, tab in pages.items():
        qid = tab.get("pageprops", {}).get("wikibase_item", "")
        break
    # ---
    return qid
