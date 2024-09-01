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


def medwiki_cat_members(cat="Category:Mdwiki Translation Dashboard articles"):
    """Retrieve members of a specified MediaWiki category.

    This function fetches the members of a given MediaWiki category. If no
    category is provided, it defaults to "Category:Mdwiki Translation
    Dashboard articles". The function processes the retrieved members by
    removing the "Md:" prefix from each member's name.

    Args:
        cat (str): The name of the MediaWiki category to retrieve members from.
            Defaults to "Category:Mdwiki Translation Dashboard articles".

    Returns:
        list: A list of member names from the specified MediaWiki category,
            with the "Md:" prefix removed.
    """

    # ---
    if not cat:
        cat = "Category:Mdwiki Translation Dashboard articles"
    # ---
    cat_members = CatDepth(cat, sitecode="medwiki", family="toolforge", depth=0, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])
    cat_members = [x.replace("Md:", "") for x in cat_members]
    return cat_members


def Create(title, text, summary):
    """Create a new page or edit an existing page on the MedWiki platform.

    This function sends a request to the MedWiki API to create or edit a
    page with the specified title, text content, and summary. It constructs
    the necessary parameters for the API call and handles the response. If
    the response cannot be parsed as JSON, it prints the raw response text.

    Args:
        title (str): The title of the page to be created or edited.
        text (str): The content to be added to the page.
        summary (str): A brief summary of the changes made.
    """

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
    `mdwiki_api.GetPageText` method. It performs several operations on the
    retrieved text, including searching for specific patterns, modifying
    references, and ensuring that the output is formatted correctly. The
    function also handles cases where the text is empty by returning an
    empty string.

    Args:
        x (str): The identifier of the page from which to retrieve text.

    Returns:
        str: The processed text from the specified page, including
        any unlinked wikibase identifiers and formatted references.
    """

    alltext = mdwiki_api.GetPageText(x)
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
    newtext = f"{unlinkedwikibase}\n\n{newtext}"
    # ---
    return newtext


def one_page(x):
    """Create or update a mediawiki page with the given title.

    This function retrieves text associated with a given title, formats it,
    and either updates an existing mediawiki page or creates a new one if it
    does not exist. The title is prefixed with "Md:" and the summary is
    generated to link back to the original title in a specific format. If
    the page already exists, it updates the content; otherwise, it creates a
    new page.

    Args:
        x (str): The title of the mediawiki page to create or update.
    """

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
    """Retrieve all pages from a cached source or load from a file.

    This function checks if a JSON file containing all pages exists. If the
    file exists, it reads and returns the contents of the file. If the file
    does not exist, it generates the pages using a caching mechanism and
    saves the result to the JSON file for future access. This ensures that
    the data can be retrieved efficiently without recalculating it every
    time.

    Returns:
        list: A list of all pages, either loaded from the JSON file
        or generated from the cache.
    """

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

    This function processes a list of pages either in parallel or
    sequentially based on the command-line arguments. If "multi" is present
    in the command-line arguments, it utilizes a multiprocessing pool to
    handle the pages concurrently. Otherwise, it processes each page one by
    one, printing the progress as it goes.

    Args:
        all_pages (list): A list of pages to be processed.

    Returns:
        None: This function does not return a value.
    """

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
    """Execute the main workflow of the application.

    This function orchestrates the main operations of the application by
    retrieving category members, fetching all pages, and filtering the pages
    based on the command-line arguments. It also prints the count of all
    pages and the count of completed tasks.
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
    """Execute the main workflow for processing pages with reference errors.

    This function retrieves a list of pages categorized under
    "Category:Pages with reference errors" and initiates the processing of
    these pages. It first calls the `medwiki_cat_members` function to obtain
    the relevant pages and then prints the number of pages to be processed.
    Finally, it invokes the `start` function to handle the processing of the
    retrieved pages.
    """

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
        one_page("COVID-19")
        # one_page("Chronic lymphocytic leukemia")
    elif "main2" in sys.argv:
        main2()
    else:
        main()
