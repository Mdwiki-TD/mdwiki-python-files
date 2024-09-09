#!/usr/bin/python3
"""
https://hashtags.wmcloud.org/json/?query=mdwikicx

بوت قواعد البيانات

python3 core8/pwb.py after_translate/mdwikicx
python3 core8/pwb.py after_translate/mdwikicx pages_users
python3 core8/pwb.py after_translate/mdwikicx justsql
python3 core8/pwb.py after_translate/mdwikicx -lang:ur

"""

import sys
import requests
import json
import re
from pathlib import Path
from newapi import printe
from newapi.page import MainPage
from mdpy.bots import en_to_md
from after_translate.bots import add_to_wd


def get_result():
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
        printe.output(f"not article.{page_title=}\t{ns=}")
        return
    # ---
    qid_in = page.get_qid()
    # ---
    if not qid_in:
        add_to_wd.add_wd(qid, "", lang, page_title)
        return
    # ---
    printe.output(f"<<blue>> {qid_in=}, {qid=}")


def main():
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg in ["lang", "-lang"]:
            lang_o = value
    # ---
    result_list = [
        {"Domain": "fr.wikipedia.org", "Timestamp": "2024-08-22T03:09:01Z", "Username": "Mr. Ibrahem", "Page_title": "Utilisateur:Mr. Ibrahem/Acute lymphoblastic leukemia", "Edit_summary": "Created by translating the page [[:mdwiki:Acute lymphoblastic leukemia|Acute lymphoblastic leukemia]]. #mdwikicx .", "Revision_ID": 217884468},
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
        # printe.output(tab)
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
