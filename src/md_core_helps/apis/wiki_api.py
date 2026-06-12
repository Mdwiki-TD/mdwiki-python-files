#!/usr/bin/python3
"""
# ---
from md_core_helps.apis import wiki_api
# wiki_api.submitAPI( params, site="en", returnjson = False )
# ---
"""
from mdwiki_api.wiki_page import NewApi

api_news = {}


def submitAPI(params, site: str="", returnjson: bool=False):
    # ---
    params["format"] = "json"
    # ---
    if site not in api_news:
        api_news[site] = NewApi(site, family="wikipedia")
        # api_news[site].Login_to_wiki()
    # ---
    json1 = api_news[site].post_params(params, addtoken=True)
    # ---
    return json1


def Get_page_qid(sitecode, title):
    # ---
    sitecode = sitecode.removesuffix("wiki")
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
    for _id, tab in pages.items():
        qid = tab.get("pageprops", {}).get("wikibase_item", "")
        break
    # ---
    return qid
