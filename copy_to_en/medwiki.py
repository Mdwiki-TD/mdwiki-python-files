#!/usr/bin/python3
"""

python3 core8/pwb.py copy_to_en/medwiki ask

tfj run copymulti --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py copy_to_en/medwiki multi"
tfj run main2 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py copy_to_en/medwiki"
tfj run nodone --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py copy_to_en/medwiki nodone"

"""
import random
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
    alltext, revid = mdwiki_api.GetPageText(x, get_revid=True)
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
    return newtext, revid


def one_page(x):
    newtext, revid = get_text(x)
    # ---
    new_title = "Md:" + x
    # ---
    x2 = x.replace(" ", "_")
    # ---
    summary = f"from [[:mdwiki:{x2}|{x}]]"
    summary = f"from [[:mdwiki:Special:Redirect/revision/{revid}|{x}]]"
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
