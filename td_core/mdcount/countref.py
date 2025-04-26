#!/usr/bin/python3
"""

إنشاء قائمة بعدد المراجع

وحفظها في Dashboard_path
+
قاعدة البيانات


python3 core8/pwb.py mdcount/countref newpages

python3 core8/pwb.py mdcount/countref -title:Esophageal_rupture

"""

import os
import sys

from apis import mdwiki_api
from newapi import printe
from mdcount.bots.links import get_links_from_cats
from mdapi_sql import sql_for_mdwiki
from mdcount.ref_words_bot import get_jsons, logaa, make_old_values, do_to_sql
from mdcount.bots.countref_bots import count_ref_from_text
# ---
if os.getenv("HOME"):
    Dashboard_path = os.getenv("HOME") + "/public_html/td"
else:
    Dashboard_path = "I:/mdwiki/mdwiki/public_html/td"
# ---
all_tab_data = {1: {}}
lead_tab_data = {1: {}}
# ---
file_all = f"{Dashboard_path}/Tables/jsons/all_refcount.json"
file_lead = f"{Dashboard_path}/Tables/jsons/lead_refcount.json"


def start_to_sql():
    return do_to_sql(all_tab_data[1], lead_tab_data[1], ty="ref")


def count_refs(title):
    # ---
    text = mdwiki_api.GetPageText(title)
    # ---
    # extend short refs
    text2 = text
    # text2 = ref.fix_ref(text, text)
    # ---
    all_c = count_ref_from_text(text2)
    # ---
    leadtext = text2.split("==")[0]
    lead_c = count_ref_from_text(leadtext, get_short=True)
    # ---
    all_tab_data[1][title] = all_c
    lead_tab_data[1][title] = lead_c
    # ---
    printe.output(f"<<green>> all:{all_c} \t lead:{lead_c}")


def from_sql(old_values):
    # ---
    que = """select title from titles_infos;"""
    # ---
    sq = sql_for_mdwiki.select_md_sql(que, return_dict=True)
    # ---
    titles2 = [q["title"] for q in sq]
    # ---
    titles = [x for x in titles2 if x not in old_values]
    # ---
    printe.output(f"<<yellow>> sql: find {len(titles2)} titles, {len(titles)} to work. ")
    # ---
    return titles


def get_links():
    # ---
    titles=[]
    # ---
    old_values = make_old_values(all_tab_data[1], lead_tab_data[1])
    # ---
    if "sql" in sys.argv:
        titles=from_sql(old_values)
    else:
        titles=get_links_from_cats()
    # ---
    if "newpages" in sys.argv:
        titles=[x for x in titles if (x not in old_values)]
    # ---
    return titles


def main():
    # ---
    all_tab_data[1], lead_tab_data[1] = get_jsons(file_all, file_lead, "ref")
    # ---
    limit = 100 if "limit100" in sys.argv else 10000
    # ---
    # python3 core8/pwb.py mdcount/countref -title:Testosterone_\(medication\)
    # ---
    vaild_links = []
    # ---
    for arg in sys.argv:
        arg, _, value=arg.partition(":")
        # ---
        if arg == "-title":
            vaild_links=[value.replace("_", " ")]
    # ---
    if not vaild_links:
        vaild_links = get_links()
    # ---
    for numb, x in enumerate(vaild_links):
        # ---
        x = x.replace("\\'", "'")
        # ---
        printe.output('------------------')
        printe.output(f'page {numb} from {len(vaild_links)}, x:{x}')
        # ---
        if numb >= limit:
            break
        # ---
        count_refs(x)
        # ---
        if numb == 10 or str(numb).endswith("00"):
            logaa(file_lead, lead_tab_data[1])
            logaa(file_all, all_tab_data[1])
    # ---
    logaa(file_lead, lead_tab_data[1])
    logaa(file_all, all_tab_data[1])
    # ---
    start_to_sql()


def test():
    # python3 core8/pwb.py mdcount/countref test
    # ---
    lead_tab_data[1]["Yemen1"]=50
    all_tab_data[1]["Yemen1"]=50
    # ---
    lead_tab_data[1]["Sana'a"]=500
    all_tab_data[1]["Sana'a"]=100
    # ---
    start_to_sql()


if __name__ == "__main__":
    if "test" in sys.argv:
        test()
        exit()
    # ---
    main()
    # ---
    if "sql" not in sys.argv:
        sys.argv.append('sql')
        # ---
        main()
