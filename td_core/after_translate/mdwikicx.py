#!/usr/bin/python3
"""
https://hashtags.wmcloud.org/json/?query=mdwikicx

بوت قواعد البيانات

python3 core8/pwb.py after_translate/mdwikicx
python3 core8/pwb.py after_translate/mdwikicx pages_users
python3 core8/pwb.py after_translate/mdwikicx justsql
python3 core8/pwb.py after_translate/mdwikicx -lang:ur

"""

import json
import logging
import re
import sys
from pathlib import Path

import requests
from after_translate.bots import add_to_wd
from mdpy.bots import en_to_md
from newapi.page import MainPage

logger = logging.getLogger(__name__)


def get_result():
    """Fetches the result from a specified URL and returns the rows of data.

    This function makes a GET request to a predefined URL to retrieve JSON
    data. It extracts the "Rows" key from the JSON response and returns its
    value. If an error occurs during the request or while processing the
    response, the function catches the exception, prints an error message,
    and returns an empty list.

    Returns:
        list: A list of rows extracted from the JSON response.
            If an error occurs, an empty list is returned.
    """

    url = "https://hashtags.wmcloud.org/json/?query=mdwikicx"
    # ---
    try:
        r = requests.get(url)
        result = r.json()
        rows = result.get("Rows", [])
        return rows

    except Exception as e:
        print(f"Exception: {e}")
    # ---
    return []


def work_one_page(x):
    """Process a single page based on the provided metadata.

    This function retrieves the QID associated with a given markdown title
    and checks if the corresponding Wikipedia page exists. If the page
    exists and is in the main namespace, it retrieves the QID of the page.
    If the page does not exist or is not in the main namespace, appropriate
    actions are taken, including logging output and potentially adding data
    to Wikidata.

    Args:
        x (dict): A dictionary containing metadata with keys "mdtitle",
            "page_title", and "lang".

    Returns:
        None: The function does not return a value but may perform side
            effects such as logging output or modifying data.
    """

    # ---
    qid = en_to_md.mdtitle_to_qid.get(x["mdtitle"], "")
    # ---
    page_title = x["page_title"]
    lang = x["lang"]
    # ---
    page = MainPage(page_title, lang, family="wikipedia")
    # ---
    if not page.exists():
        return
    # ---
    ns = page.namespace()
    # ---
    if ns != 0:
        logger.info(f"not article.{page_title=}\t{ns=}")
        return
    # ---
    qid_in = page.get_qid()
    # ---
    if not qid_in:
        add_to_wd.add_wd(qid, "", lang, page_title)
        return
    # ---
    logger.info(f"<<blue>> {qid_in=}, {qid=}")


def main():
    """Main function to process command-line arguments and extract specific
    information
    from a predefined result list.  This function iterates through command-
    line arguments to check for a specified language option. It then
    processes a hardcoded list of results, extracting relevant data such as
    domain, timestamp, username, page title, and edit summary. The extracted
    information is stored in a structured format and saved to a JSON file.
    Additionally, the function filters out entries based on specific
    usernames.
    """

    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg in ["lang", "-lang"]:
            lang_o = value
    # ---
    result_list = [
        {
            "Domain": "fr.wikipedia.org",
            "Timestamp": "2024-08-22T03:09:01Z",
            "Username": "Mr. Ibrahem",
            "Page_title": "Utilisateur:Mr. Ibrahem/Acute lymphoblastic leukemia",
            "Edit_summary": "Created by translating the page [[:mdwiki:Acute lymphoblastic leukemia|Acute lymphoblastic leukemia]]. #mdwikicx .",
            "Revision_ID": 217884468,
        },
    ]
    # ---
    _result_keys = {
        "Domain": "ar.wikipedia.org",
        "Timestamp": "2024-09-04T01:33:31Z",
        "Username": "Mr. Ibrahem",
        "Page_title": "مستخدم:Mr. Ibrahem/Tropicamide",
        "Edit_summary": 'Created by translating the page "[[:mdwiki:Special:Redirect/revision/5210|Tropicamide]] to:ar #mdwikicx"',
        "Revision_ID": 67801114,
    }
    # ---
    titles = []
    # ---
    for x in result_list:
        # ---
        lang = x.get("Domain", "").replace(".wikipedia.org", "")
        # ---
        tab = {
            "lang": lang,
            "timestamp": x.get("Timestamp", "").split("T")[0],
            "username": x.get("Username", ""),
            "page_title": x.get("Page_title", ""),
            "mdtitle": "",
        }
        # ---
        md_title_find = re.search(r"\|(.*?)\]\]", x.get("Edit_summary", ""))
        # ---
        if md_title_find:
            tab["mdtitle"] = md_title_find.group(1)
        # ---
        if tab["username"].find("Mr. Ibrahem") != -1 or tab["username"].find("Doc James") != -1:
            continue
        # ---
        # logger.info(tab)
        # ---
        titles.append(tab)
    # ---
    with open(Path(__file__).parent / "titles.json", "w", encoding="utf-8") as f:
        json.dump(titles, f, ensure_ascii=False)
    # ---
    for x in titles:
        # ---
        work_one_page(x)


if __name__ == "__main__":
    main()
