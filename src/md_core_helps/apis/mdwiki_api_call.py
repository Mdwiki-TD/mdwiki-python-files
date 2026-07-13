#!/usr/bin/python3
"""
# revid    = mdwiki_api.GetRevid(title)
"""
import logging

from mdwiki_api.mdwiki_page import NewApi, md_MainPage

logger = logging.getLogger(__name__)

api_new = NewApi("www", family="mdwiki")

def post_s(params, addtoken: bool=False, files=None):
    # ---
    params["format"] = "json"
    params["utf8"] = 1
    # ---
    json1 = api_new.post_params(params, addtoken=addtoken, files=files)
    # ---
    return json1


def page_put(
    newtext: str="",
    summary: str="",
    title: str="",
    minor: str="",
    nocreate: int=1,
    **kwargs,
):
    # ---
    page = md_MainPage(title, "www", family="mdwiki")
    exists = page.exists()
    # ---
    save_page = page.save(newtext=newtext, summary=summary, nocreate=nocreate, minor=minor)
    # ---
    return save_page

def create_Page(
    text: str,
    summary,
    title,
    ask,
    **kwargs,
):
    # ---
    page = md_MainPage(title, "www", family="mdwiki")
    # ---
    create = page.Create(text=text, summary=summary)
    # ---
    return create


def wordcount(title, srlimit: str="30"):
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


def GetPageText(title, redirects: bool=False, get_revid: bool=False):
    """Retrieve the wikitext of a specified page from a wiki.

    This function sends a request to a wiki API to retrieve the wikitext of
    a page identified by its title. It can handle redirects and can
    optionally return the revision ID of the page. If the page does not
    exist or cannot be parsed, appropriate messages are logged.

    Args:
        title (str): The title of the page to retrieve.
        redirects (bool?): Whether to follow redirects. Defaults to False.
        get_revid (bool?): Whether to return the revision ID along with the wikitext.
            Defaults to False.

    Returns:
        str: The wikitext of the specified page.
        tuple: A tuple containing the wikitext and the revision ID if get_revid is
            True.
    """

    # logger.info( '**GetarPageText: ')
    # ---
    params = {
        "action": "parse",
        # "prop": "wikitext|sections",
        "prop": "wikitext|revid",
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
    json1 = post_s(params) or {}
    if json1:
        text = json1.get("parse", {}).get("wikitext", {}).get("*", "")
    else:
        logger.info("no parse in json1:")
        logger.info(json1)
    # ---
    if not text:
        logger.info(f'page {title} text == "".')
    # ---
    if get_revid:
        return text, json1.get("parse", {}).get("revid", 0)
    # ---
    return text


def GetRevid(title):
    """Retrieve the revision ID for a given page title.

    This function sends a request to a specified API to retrieve the
    revision ID associated with the provided page title. It constructs a
    parameters dictionary for the API call and processes the response to
    extract the revision ID. If the response does not contain a valid
    revision ID, it returns an empty string.

    Args:
        title (str): The title of the page for which to retrieve the revision ID.

    Returns:
        str: The revision ID of the specified page title, or an empty string if not
            found.
    """

    # ---
    params = {"action": "parse", "prop": "revid", "page": title}
    # ---
    json1 = post_s(params) or {}
    if json1:
        revid = json1.get("parse", {}).get("revid", 0)
        return revid
    # ---
    return ""


def Get_page_links(title, namespace: str = "0", limit: Union[int, str] = "max"):
    # ---
    logger.info(f' for title:"{title}", limit:"{limit}",namespace:"{namespace}"')
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
    json1 = post_s(params) or {}
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
        logger.info("mdwiki_api.py no json1")
    # ---
    logger.info(f"mdwiki_api.py : find {len(Main_table['links'])} pages.")
    # ---
    return Main_table


def Get_template_pages(title, namespace: str = "*", limit: Union[int, str] = "max"):
    return api_new.Get_template_pages(title, namespace=namespace)


def Get_All_pages(start, namespace: str = "0", limit: Union[int, str] = "max", apfilterredir: str = "", limit_all: int = 0) -> list[str]:
    return api_new.Get_All_pages(
        start=start,
        namespace=namespace,
        limit=limit,
        apfilterredir=apfilterredir,
        limit_all=limit_all,
    )


def Get_UserContribs(user, limit: Union[int, str] = "max", namespace: str = "*", ucshow: str = ""):
    return api_new.UserContribs(user, limit=limit, namespace=namespace, ucshow=ucshow)


def get_redirect(liste):
    return api_new.get_titles_redirects(liste)


def Find_pages_exists_or_not(liste):
    return api_new.Find_pages_exists_or_not(liste)
