#!/usr/bin/python3
"""

إنشاء قائمة بعدد المراجع

python3 $HOME/pybot/md_core/mdcount/countref.py newpages

python3 core8/pwb.py mdcount/countref newpages

python3 core8/pwb.py mdcount/countref -title:Esophageal_rupture

"""

import os
import json
import sys
from pathlib import Path


from mdapi_sql import sql_for_mdwiki
from apis import mdwiki_api
from newapi import printe
from mdcount.bots.regex_scanner import RegexScanner
from mdcount.bots.links import get_links_from_cats
from mdpyget.bots.to_sql import to_sql

if os.getenv("HOME"):
    Dashboard_path = os.getenv("HOME") + "/public_html/td"
else:
    Dashboard_path = "I:/mdwiki/mdwiki/public_html/td"
# ---
all_ref = {}
lead_ref = {}
vaild_links = {1: []}
# ---
file_all = f"{Dashboard_path}/Tables/jsons/all_refcount.json"
file_lead = f"{Dashboard_path}/Tables/jsons/lead_refcount.json"
# ---
a = {}
# ---
with open(file_all, "r", encoding="utf-8") as f:
    a = json.load(f)
# ---
all_ref = {x: ref for x, ref in a.items() if ref > 0}
# ---
la = {}
# ---
with open(file_lead, "r", encoding="utf-8") as f:
    la = json.load(f)
# ---
lead_ref = {x: ref for x, ref in la.items() if ref > 0}
# ---
# list for titles in both all_ref and lead_ref
list_fu = list(set(all_ref.keys()) & set(lead_ref.keys()))
# ---
# remove duplicates from list
list_fu = list(set(list_fu))
list_ma = {1: [x for x in list_fu if (x in all_ref and x in lead_ref)]}


def get_refs_new(text):
    ref_list = []
    # ---
    scanner = RegexScanner(r"(?i)<ref(?P<name>[^>/]*)>(?P<content>.*?)</ref>", text)
    # ---
    for m in scanner.requests:
        # ---
        name = m.get("name", "")
        content = m.get("content", "")
        # ---
        if name.strip() != "":
            if name.strip() not in ref_list:
                ref_list.append(name.strip())
        elif content.strip() != "":
            if content.strip() not in ref_list:
                ref_list.append(content.strip())
    # ---
    printe.output(f"len of get_refs_new : {len(ref_list)}")
    # ---
    return ref_list


def get_short_refs(text):
    # ---
    scanner = RegexScanner(r"<ref\s*name\s*=\s*[\"\']*(?P<name>[^>]*)[\"\']*\s*\/\s*>", text)
    # ---
    ref_list = scanner.attr_scan("name")
    # ---
    # printe.output(f"len of get_short_refs : {len(ref_list)}")
    # ---
    return ref_list


def count_ref_from_text(text, get_short=False):
    # ---
    ref_list = []
    # ---
    # short_list = get_short_refs(text)
    # ---
    if get_short:
        short_list = get_short_refs(text)
        ref_list.extend(short_list)
    # ---
    refs = get_refs_new(text)
    # ---
    ref_list.extend(refs)
    # ---
    return len(ref_list)


def count_refs(title):
    # ---
    text = mdwiki_api.GetPageText(title)
    # ---
    # extend short refs
    text2 = text
    # text2 = ref.fix_ref(text, text)
    # ---
    all_c = count_ref_from_text(text2)
    all_ref[title] = all_c
    # ---
    leadtext = text2.split("==")[0]
    lead_c = count_ref_from_text(leadtext, get_short=True)
    # ---
    lead_ref[title] = lead_c
    # ---
    printe.output(f"<<green>> all:{all_c} \t lead:{lead_c}")


def logaa(file, table):
    with open(file, "w", encoding="utf-8") as outfile:
        json.dump(table, outfile, sort_keys=True, indent=2)
    # ---
    printe.output(f"<<green>> {len(table)} lines to {file}")


def from_sql():
    # ---
    que = """select title, word from pages;"""
    # ---
    sq = sql_for_mdwiki.select_md_sql(que, return_dict=True)
    # ---
    titles2 = [q["title"] for q in sq]
    # ---
    titles = [x for x in titles2 if x not in list_ma[1]]
    # ---
    printe.output(f"<<yellow>> sql: find {len(titles2)} titles, {len(titles)} to work. ")
    return titles


def get_links():
    # ---
    titles = []
    # ---
    if "sql" in sys.argv:
        titles = from_sql()
    else:
        titles = get_links_from_cats()
    # ---
    if "newpages" in sys.argv:
        titles = [x for x in titles if (x not in list_ma[1])]
    # ---
    return titles


def mai():
    # ---
    numb = 0
    # ---
    limit = 100 if "limit100" in sys.argv else 10000
    # ---
    # python3 core8/pwb.py mdcount/countref -title:Testosterone_\(medication\)
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        # ---
        if arg == "-title":
            vaild_links[1] = [value.replace("_", " ")]
    # ---
    if not vaild_links[1]:
        vaild_links[1] = get_links()
    # ---
    for x in vaild_links[1]:
        # ---
        numb += 1
        # ---
        if numb >= limit:
            break
        # ---
        printe.output(" p %d from %d: for %s:" % (numb, len(vaild_links[1]), x))
        # ---
        count_refs(x)
        # ---
        if numb == 10 or str(numb).endswith("00"):
            logaa(file_lead, lead_ref)
            logaa(file_all, all_ref)
        # ---
    # ---
    logaa(file_lead, lead_ref)
    logaa(file_all, all_ref)
    # ---
    start_to_sql()


def start_to_sql():
    data2 = [{"r_title": x, "r_lead_refs": v, "r_all_refs": all_ref.get(x, 0)} for x, v in lead_ref.items()]
    # ---
    to_sql(data2, "refs_counts", ["r_title", "r_lead_refs", "r_all_refs"], title_column="r_title")


def test():
    # python3 core8/pwb.py mdcount/countref test
    # ---
    lead_ref["Yemen1"] = 50
    all_ref["Yemen1"] = 50
    # ---
    lead_ref["Sana'a"] = 500
    all_ref["Sana'a"] = 100
    # ---
    start_to_sql()


if __name__ == "__main__":
    if "test" in sys.argv:
        test()
    else:
        mai()
