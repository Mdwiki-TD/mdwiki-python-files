#!/usr/bin/python3
"""

python3 core8/pwb.py copy_to_en/medwiki nodone ask
python3 core8/pwb.py copy_to_en/medwiki nodone slash ask

tfj run copymulti --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py copy_to_en/medwiki multi"
tfj run main2 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py copy_to_en/medwiki"
tfj run nodone --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py copy_to_en/medwiki nodone"

"""
import random
import requests
import json
import sys
import re
from pathlib import Path
from multiprocessing import Pool
from apis import cat_cach
from apis import mdwiki_api
from newapi.super import super_page
from newapi.super import catdepth_new
from copy_to_en.bots import medwiki_account
from copy_to_en.bots import alltext_changes  # text = alltext_changes.do_alltext_changes(text)
from copy_to_en.bots import text_changes  # text = text_changes.work(text)
from copy_to_en.bots.ref import fix_ref  # text = fix_ref(first, alltext)
from mdapi_sql import sql_for_mdwiki

# ---
User_tables = {
    "username": medwiki_account.username,
    "password": medwiki_account.password,
}
# ---
catdepth_new.User_tables["toolforge"] = User_tables
super_page.User_tables["toolforge"] = User_tables
# ---
CatDepth = catdepth_new.subcatquery
MainPage = super_page.MainPage

Dir = Path(__file__).parent

text_cache = {}
revid_cache = {}
un_wb_tag_cache = {}

mdwiki_cats = sql_for_mdwiki.get_db_categories()
# {'RTT': 1, 'RTTCovid': 0, 'RTTHearing': 0, 'RTTOSH': 0, 'World Health Organization essential medicines': 0, 'WHRTT': 0, 'RTTILAE': 0, 'RTTDZ': 0}
# print(mdwiki_cats)


def make_new_r3_token():
    # ---
    end_api = "https://medwiki.toolforge.org/w/api.php"
    # ---
    r3_params = {
        "format": "json",
        "action": "query",
        "meta": "tokens",
    }
    # ---
    req = requests.get(end_api, r3_params)
    # ---
    if not req:
        return False
    # ---
    try:
        data = req.json()
        csrftoken = data.get("query", {}).get("tokens", {}).get("csrftoken", "")
        return csrftoken
    except Exception as e:
        print(f"Exception: {e}")
    # ---
    return ""


def just_save(title, text, summary, csrftoken):
    # ---
    end_api = "https://medwiki.toolforge.org/w/api.php"
    # ---
    params = {
        "action": "edit",
        "title": title,
        "text": text,
        "summary": summary,
        "format": "json",
        "token": csrftoken,
    }
    # ---
    response = requests.post(end_api, data=params)
    # ---
    try:
        print(response.json())
    except Exception as e:
        print(f"Exception: {e}")
        print(response.text)


def get_cats(alltext):
    # ---
    cats = []
    # ---
    for category in mdwiki_cats:
        # ---
        mat = re.search(rf"\[\[Category:{category}(\]\]|\|)", alltext, re.IGNORECASE)
        # ---
        if mat:
            cats.append(category)
    # ---
    cats = list(set(cats))
    # ---
    # if len(cats) > 1 and "RTT" in cats: cats.remove("RTT")
    # ---
    cats_text = "\n".join([f"[[Category:{x}]]" for x in cats])
    # ---
    return cats_text


def medwiki_cat_members(cat="Category:Mdwiki Translation Dashboard articles"):
    # ---
    if not cat:
        cat = "Category:Mdwiki Translation Dashboard articles"
    # ---
    cat_members = CatDepth(cat, sitecode="medwiki", family="toolforge", depth=0, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])
    cat_members = [x.replace("Md:", "") for x in cat_members]
    return cat_members


def get_text_revid(x):
    alltext, revid = mdwiki_api.GetPageText(x, get_revid=True)
    # ---
    text_cache[x] = alltext
    revid_cache[x] = revid
    # ---
    return alltext, revid


def get_un_wb_tag(alltext, x):
    # search for text like {{#unlinkedwikibase:id=Q423364}}
    pattern = r"\{\{#unlinkedwikibase:id=Q[0-9]+\}\}"
    # ---
    match = re.search(pattern, alltext)
    # ---
    unlinkedwikibase = match.group(0) if match else ""
    # ---
    # matches = re.findall(pattern, alltext)
    # for m in matches:
    #     unlinkedwikibase = m
    #     break
    # ---
    un_wb_tag_cache[x] = unlinkedwikibase
    # ---
    return unlinkedwikibase


def get_text(x):
    """Retrieve and process text from a specified page.

    This function fetches the text content of a page using the
    `mdwiki_api.GetPageText` method. It processes the retrieved text to
    extract and format specific information, including handling unlinked
    Wikibase IDs and adjusting the infobox formatting. The function also
    ensures that references are properly formatted and included in the
    output.

    Args:
        x (str): The identifier of the page from which to retrieve text.

    Returns:
        tuple: A tuple containing the processed text and the revision ID
        of the page.
    """
    alltext, revid = get_text_revid(x)
    # ---
    if not alltext:
        print("no text: " + x)
        return "", ""
    # ---
    page_cats = get_cats(alltext)
    # ---
    unlinkedwikibase = get_un_wb_tag(alltext, x)
    # ---
    first = alltext.split("==")[0].strip()
    # ---
    first = first + "\n\n==References==\n<references />"
    newtext = first
    # ---
    newtext = fix_ref(first, alltext)
    # ---
    newtext = text_changes.do_text_fixes(newtext)
    # ---
    newtext += "\n[[Category:Mdwiki Translation Dashboard articles]]"
    # ---
    revid_temp = f"{{{{mdwiki revid|{revid}}}}}"
    # ---
    newtext = f"{unlinkedwikibase}\n{revid_temp}\n{newtext}\n{page_cats}"
    # ---
    return newtext, revid


def one_page(x):
    newtext, revid = get_text(x)
    # ---
    new_title = "Md:" + x
    # ---
    titles = {
        new_title: newtext,
    }
    # ---
    if new_title.find("/") != -1:
        new_title_all = f"Md:{x}/fulltext"
        # ---
        alltext = text_cache.get(x)
        # ---
        if alltext:
            unlinked_tag = un_wb_tag_cache.get(x, "")
            # ---
            alltext = alltext_changes.do_all_text(alltext, revid, unlinked_tag)
            titles[new_title_all] = alltext
        else:
            print(f"no text:{new_title_all}")
    # ---
    x2 = x.replace(" ", "_")
    # ---
    summary = f"from [[:mdwiki:{x2}|{x}]]"
    summary = f"from [[:mdwiki:Special:Redirect/revision/{revid}|{x}]]"
    # ---
    crftoken = make_new_r3_token()
    # ---
    for title, text2 in titles.items():
        # Create(new_title, newtext, summary)
        # # ---
        if text2 == "":
            print("no text: " + title)
            continue
        # # ---
        if "just_save" in sys.argv:
            just_save(title, text2, summary, crftoken)
            continue
        # # ---
        # return
        page = MainPage(title, "medwiki", family="toolforge")
        # ---
        if page.exists():
            _p_t = page.get_text()
            # ---
            if _p_t == text2:
                print("page exists: " + title)
                continue
            # ---
            page.save(text2, summary=summary, nocreate=0)
        else:
            print("page not found: " + title)
            page.Create(text=text2, summary=summary)


def get_all():
    file = Dir / "all_pages.json"
    # ----
    if file.exists() and "nodone" not in sys.argv:
        return json.loads(file.read_text())
    # ----
    all_pages = cat_cach.make_cash_to_cats(return_all_pages=True, print_s=False)
    # ---
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(all_pages))
    # ---
    return all_pages


def start(all_pages):
    """Start processing a list of pages.

    This function shuffles the input list of pages randomly and then
    processes each page. If the script is run with the "multi" argument, it
    utilizes multiprocessing to handle the pages in parallel. Otherwise, it
    processes each page sequentially, printing the progress as it goes.

    Args:
        all_pages (list): A list of pages to be processed.

    Returns:
        None: This function does not return a value.
    """

    # ---
    if "slash" in sys.argv:
        all_pages = [x for x in all_pages if x.find("/") != -1]
    # ---
    # sort all_pages randmly
    random.shuffle(all_pages)
    # ---
    if "multi" in sys.argv:
        pool = Pool(processes=2)
        pool.map(one_page, all_pages)
        pool.close()
        pool.terminate()
        return
    # ---
    for n, x in enumerate(all_pages):
        print(f"{n}/{len(all_pages)} : {x}")
        # ---
        one_page(x)


def main():
    """Main entry point for the application.

    This function orchestrates the workflow of the application by calling
    various helper functions to retrieve and process data. It first gathers
    a list of completed categories, then retrieves all available pages. If
    the "nodone" argument is not provided, it filters out the completed
    pages from the list of all pages. Finally, it initiates the processing
    of the remaining pages and saves the revisions to a JSON file.
    """
    # ---
    all_pages = get_all()
    # ---
    print(f"all_pages: {len(all_pages)}")
    # ---
    if "nodone" not in sys.argv:
        done = medwiki_cat_members()
        # ---
        print(f" done: {len(done)}. add 'nodone' to sys.argv to skip find done pages.")
        # ---
        all_pages = [x for x in all_pages if x not in done]
    # ---
    start(all_pages)


def main2():
    # ---
    cat = "Category:Pages with reference errors"
    # ---
    to_work = medwiki_cat_members(cat)
    # ---
    print(f"to_works: {len(to_work)}")
    # ---
    start(to_work)


if __name__ == "__main__":
    if "test" in sys.argv:
        one_page("Sudden infant death syndrome")
        one_page("Menopause")
        one_page("Panic attack")
    elif "main2" in sys.argv:
        main2()
    else:
        main()
