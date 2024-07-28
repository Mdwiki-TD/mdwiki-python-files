#!/usr/bin/python3
"""

"""
from newapi import printe
from newapi.mdwiki_page import MainPage as md_MainPage, NEW_API

api_new = NEW_API("www", family="mdwiki")
api_new.Login_to_wiki()

# json1    = api_new.post_params(params, addtoken=False)
# login    = api_new.Login_to_wiki()
# move_it  = api_new.move(old_title, to, reason="", noredirect=False, movesubpages=False)
# pages    = api_new.Find_pages_exists_or_not(liste, get_redirect=False)
# pages    = api_new.Get_All_pages(start='', namespace="0", limit="max", apfilterredir='', limit_all=0)
# all_pages= api_new.Get_All_pages_generator(start="", namespace="0", limit="max", filterredir="", ppprop="", limit_all=100000)
# search   = api_new.Search(value='', ns="", offset='', srlimit="max", RETURN_dict=False, addparams={})
# newpages = api_new.Get_Newpages(limit="max", namespace="0", rcstart="", user='')
# usercont = api_new.UserContribs(user, limit=5000, namespace="*", ucshow="")
# l_links  = api_new.Get_langlinks_for_list(titles, targtsitecode="", numbes=50)
# text_w   = api_new.expandtemplates(text)
# subst    = api_new.Parse_Text('{{subst:page_name}}', title)
# extlinks = api_new.get_extlinks(title)
# revisions= api_new.get_revisions(title)
# logs     = api_new.get_logs(title)
# wantedcategories  = api_new.querypage_list(qppage='Wantedcategories|Wantedfiles', qplimit="max", Max=5000)
# pages  = api_new.Get_template_pages(title, namespace="*", Max=10000)
# pages_props  = api_new.pageswithprop(pwppropname="unlinkedwikibase_id", Max=None)
# img_url  = api_new.Get_image_url(title)
# added    = api_new.Add_To_Bottom(text, summary, title, poss="Head|Bottom")
# titles   = api_new.get_titles_redirects(titles)


def post_s(params, addtoken=False, files=None):
    # ---
    params["format"] = "json"
    params["utf8"] = 1
    # ---
    json1 = api_new.post_params(params, addtoken=addtoken, files=files)
    # ---
    return json1


def page_put(newtext="", summary="", title="", minor="", nocreate=1, **kwargs):
    # ---
    page = md_MainPage(title, "www", family="mdwiki")
    exists = page.exists()
    # ---
    save_page = page.save(newtext=newtext, summary=summary, nocreate=nocreate, minor=minor)
    # ---
    return save_page


def Add_To_Bottom(appendtext, summary, title, **kwargs):
    return api_new.Add_To_Bottom(appendtext, summary, title, poss="Bottom")


def create_Page(text, summary, title, ask, **kwargs):
    # ---
    page = md_MainPage(title, "www", family="mdwiki")
    # ---
    create = page.Create(text=text, summary=summary)
    # ---
    return create


def wordcount(title, srlimit="30"):
    # srlimit = "30"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": title,
        "srlimit": srlimit,
        "format": "json",
    }
    data = post_s(params)
    # ---
    if not data:
        return 0
    # ---
    search = data.get("query", {}).get("search", [])
    # ---
    words = 0
    # ---
    for pag in search:
        tit = pag["title"]
        if tit == title:
            count = pag["wordcount"]
            words = count
            break
    # ---
    return words


def GetPageText(title, redirects=False):
    # printe.output( '**GetarPageText: ')
    # ---
    params = {
        "action": "parse",
        # "prop": "wikitext|sections",
        "prop": "wikitext",
        "page": title,
        # "redirects": 1,
        # "normalize": 1,
    }
    # ---
    if redirects:
        params["redirects"] = 1
    # ---
    text = ""
    # ---
    json1 = post_s(params)
    if json1:
        text = json1.get("parse", {}).get("wikitext", {}).get("*", "")
    else:
        printe.output("no parse in json1:")
        printe.output(json1)
    # ---
    if not text:
        printe.output(f'page {title} text == "".')
    # ---
    return text


def Get_page_links(title, namespace="0", limit="max"):
    # ---
    printe.output(f'Get_page_links for title:"{title}", limit:"{limit}",namespace:"{namespace}"')
    # ---
    params = {
        "action": "query",
        "prop": "links",
        "titles": title,
        "plnamespace": namespace,
        "pllimit": limit,
        "converttitles": 1,
    }
    # ---
    json1 = post_s(params)
    # ---
    Main_table = {
        "links": {},
        "normalized": [],
        "redirects": [],
    }
    # ---
    if json1:
        # ---
        query = json1.get("query", {})
        Main_table["normalized"] = query.get("normalized", [])
        Main_table["redirects"] = query.get("redirects", [])
        # ---
        pages = query.get("pages", {})
        # ---
        for page in pages:
            tab = pages[page]
            for pa in tab.get("links", []):
                Main_table["links"][pa["title"]] = {"ns": pa["ns"], "title": pa["title"]}
    else:
        printe.output("mdwiki_api.py no json1")
    # ---
    printe.output(f"mdwiki_api.py Get_page_links : find {len(Main_table['links'])} pages.")
    # ---
    return Main_table


def Get_template_pages(title, namespace="*", limit="max"):
    return api_new.Get_template_pages(title, namespace=namespace)


def Get_All_pages(start, namespace="0", limit="max", apfilterredir="", limit_all=0):
    return api_new.Get_All_pages(start=start, namespace=namespace, limit=limit, apfilterredir=apfilterredir, limit_all=limit_all)


def Get_UserContribs(user, limit="max", namespace="*", ucshow=""):
    return api_new.UserContribs(user, limit=limit, namespace=namespace, ucshow=ucshow)


def get_redirect(liste):
    return api_new.get_titles_redirects(liste)


def Find_pages_exists_or_not(liste):
    return api_new.Find_pages_exists_or_not(liste)
