#!/usr/bin/python3
"""

python3 core8/pwb.py copy_to_en/medwiki ask

tfj run copymulti --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py copy_to_en/medwiki multi"
tfj run main2 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py copy_to_en/medwiki main2"

"""

import json
import sys
import re
import requests
from pathlib import Path
from multiprocessing import Pool
from apis import cat_cach
from apis import mdwiki_api
from newapi.super import super_page
from newapi.super import catdepth_new
from copy_to_en import medwiki_account

from copy_to_en import text_changes  # text = text_changes.work(text)
from copy_to_en.ref import fix_ref  # text = fix_ref(first, alltext)

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
revids = {}


def medwiki_cat_members(cat="Category:Mdwiki Translation Dashboard articles"):
    # ---
    if not cat:
        cat = "Category:Mdwiki Translation Dashboard articles"
    # ---
    cat_members = CatDepth(cat, sitecode="medwiki", family="toolforge", depth=0, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])
    cat_members = [x.replace("Md:", "") for x in cat_members]
    return cat_members


def Create(title, text, summary):
    # ---
    end_api = "https://medwiki.toolforge.org/w/api.php"
    # ---
    params = {
        "action": "edit",
        "title": title,
        "text": text,
        "summary": summary,
        "format": "json",
        "token": "\\\\+",
    }
    # ---
    response = requests.post(end_api, data=params)
    # ---
    try:
        print(response.json())
    except:
        print(response.text)


def get_text(x):
    """Retrieve and process text from a specified page.

    This function fetches the text content of a page identified by the
    parameter `x` using the `mdwiki_api.GetPageText` method. It processes
    the retrieved text by searching for specific patterns, modifying
    references, and ensuring that the output is formatted correctly. The
    function also handles cases where the page may not contain any text,
    returning an empty string in such instances.

    Args:
        x (str): The identifier of the page from which to retrieve text.

    Returns:
        str: The processed text content from the specified page. If no
        text is found, an empty string is returned.
    """

    alltext, revid = mdwiki_api.GetPageText(x, get_revid=True)
    # ---
    revids[x] = revid
    # ---
    if not alltext:
        print("no text: " + x)
        return ""
    # ---
    unlinkedwikibase = ""
    # search for text like {{#unlinkedwikibase:id=Q423364}}
    pattern = r"\{\{#unlinkedwikibase:id=Q[0-9]+\}\}"
    matches = re.findall(pattern, alltext)
    for m in matches:
        unlinkedwikibase = m
        break
    # ---
    first = alltext.split("==")[0].strip()
    # ---
    first = first + "\n\n==References==\n<references />"
    newtext = first
    # ---
    newtext = fix_ref(first, alltext)
    # ---
    newtext = text_changes.work(newtext)
    newtext = newtext.replace("{{Drugbox", "{{Infobox drug")
    newtext = newtext.replace("{{drugbox", "{{Infobox drug")
    # ---
    # remove any text before {{Infobox or {{Drugbox
    if newtext.lower().find("{{infobox") != -1:
        newtext = newtext[newtext.lower().find("{{infobox") :]
    elif newtext.lower().find("{{drugbox") != -1:
        newtext = newtext[newtext.lower().find("{{drugbox") :]
    # ---
    revid_temp = f"{{{{mdwiki revid|{revid}}}}}"
    # ---
    newtext = f"{unlinkedwikibase}\n{revid_temp}\n{newtext}"
    # ---
    return newtext


def one_page(x):
    newtext = get_text(x)
    # ---
    new_title = "Md:" + x
    # ---
    x2 = x.replace(" ", "_")
    # ---
    summary = f"from [[:mdwiki:{x2}|{x}]]"
    # ---
    # Create(new_title, newtext, summary)
    # # ---
    # return
    page = MainPage(new_title, "medwiki", family="toolforge")
    # ---
    if page.exists():
        _p_t = page.get_text()
        # ---
        page.save(newtext, summary=summary, nocreate=0)
    else:
        print("page not found: " + new_title)
        page.Create(text=newtext, summary=summary)


def get_all():
    file = Dir / "all_pages.json"
    # ----
    if file.exists():
        return json.loads(file.read_text())
    # ----
    all_pages = cat_cach.make_cash_to_cats(return_all_pages=True, print_s=False)
    # ---
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(all_pages))
    # ---
    return all_pages


def start(all_pages):
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
    done = medwiki_cat_members()
    # ---
    all_pages = get_all()
    # ---
    print(f"all_pages: {len(all_pages)}, done: {len(done)}")
    # ---
    if "nodone" not in sys.argv:
        all_pages = [x for x in all_pages if x not in done]
    # ---
    start(all_pages)
    # ---
    file = Dir / "all_pages_revids.json"
    # ---
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(revids), ensure_ascii=False)
    # ---


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
        # one_page("Posaconazole")
        one_page("Tropicamide")
        # one_page("Chronic lymphocytic leukemia")
    elif "main2" in sys.argv:
        main2()
    else:
        main()
