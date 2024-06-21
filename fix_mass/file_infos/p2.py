"""

from fix_mass.file_infos.pages import get_files

python3 core8/pwb.py fix_mass/file_infos/p2 debug

"""
import sys
import json
from pathlib import Path
from newapi import printe
from newapi.ncc_page import NEW_API

Dir = Path(__file__).parent

api_new = NEW_API("www", family="nccommons")
api_new.Login_to_wiki()

debug = "debug" in sys.argv
number = 10 if debug and "no" not in sys.argv else 500
len_all_files = {1: 0}


def dump_continues(params_continue):
    if debug:
        return
    try:
        with open(Dir / "params_continue.json", "w", encoding="utf-8") as f:
            json.dump(params_continue, f, indent=2)
    except Exception as e:
        printe.output(e)


def get_continues():
    try:
        with open(Dir / "params_continue.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        printe.output(e)
        return {}


def printdebug(s):
    if debug:
        printe.output(s)


def get_file_rev(title):
    # ---
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": title,
        "utf8": 1,
        "formatversion": "2",
        "rvprop": "content",
        "rvslots": "main",
        "rvlimit": "10",
        "rvdir": "newer",
    }
    # ---
    data = api_new.post_params(params)
    # ---
    error = data.get("error", {})
    if error:
        printe.output(json.dumps(error, indent=2))
    # ---
    pages = data.get("query", {}).get("pages", [])
    # ---
    img_id = ""
    urlx = ""
    # ---
    for page in pages:
        title = page.get("title")
        # ---
        revisions = page.get("revisions")
        # ---
        if not revisions:
            continue
        # ---
        for x in revisions:
            _content = x["slots"]["main"]["content"]
            # ---
            # # if not img_id: img_id = match_id(_content, title)
            # ---
            # if not urlx:
            # url = get_img_url_from_content(_content)
            # if url: urlx = url
            # ---
            if img_id and urlx:
                break
    # ---
    data = {"url": urlx, "id": img_id}
    # ---
    return data


def one_rev(title, x):
    # ---
    return {
        "title": title,
        "parentid": x.get("parentid", ""),
        "content": x.get("slots", {}).get("main", {}).get("content", ""),
    }


def get_data(params_continue=None):
    # ---
    cat_title = "Category:Uploads by Mr. Ibrahem"
    # ---
    if params_continue:
        printe.output(f"<<blue>> add params_continue: len_all_files: {len_all_files[1]}")
        dump_continues(params_continue)
    # ---
    # get cat members
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageprops|revisions",
        "generator": "categorymembers",
        "utf8": 1,
        "formatversion": "2",
        "rvprop": "content|ids|timestamp",
        "rvslots": "main",
        "rvdir": "older",
        "gcmtitle": cat_title,
        "gcmprop": "title",
        "gcmtype": "file",
        "gcmlimit": number,
        "gcmdir": "older",
    }
    # ---
    # params["rvlimit"] = number # error: "titles", "pageids" or a generator was used to supply multiple pages, but the "rvlimit", "rvstartid", "rvendid", "rvdir=newer", "rvuser", "rvexcludeuser", "rvstart", and "rvend" parameters may only be used on a single page.
    # ---
    max_do = 11
    pages = []
    # ---
    while params_continue or max_do == 11:
        # ---
        max_do -= 1
        # ---
        # printdebug(f"max_do:{max_do}")
        # ---
        if max_do == 0:
            break
        # ---
        if params_continue:
            params.update(params_continue)
        # ---
        data = api_new.post_params(params)
        # ---
        pages.extend(data.get("query", {}).get("pages", []))
        # ---
        error = data.get("error", {})
        # ---
        if error:
            printe.output(json.dumps(error, indent=2))
        # ---
        if data.get("continue"):
            params_continue = data["continue"]
        # ---
        del data
    # ---
    printdebug(f"len(pages): {len(pages)}")
    # ---
    len_all_files[1] += len(pages)
    # ---
    return pages, params_continue


def get_files(params_continue=None, load_json=False):
    # ---
    if load_json and not params_continue:
        params_continue = get_continues()
    # ---
    printdebug("get_files")
    # ---
    pages, continues = get_data(params_continue)
    # ---
    for page in pages:
        title = page["title"]
        # ---
        revisions = page.get("revisions", [{}])[0]
        # ---
        tab = one_rev(title, revisions)
        # ---
        yield tab
    # ---
    if continues:
        yield from get_files(continues)


def test():
    for x in get_files():
        pass


if __name__ == "__main__":
    test()
