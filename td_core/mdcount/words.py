#!/usr/bin/python3
"""

إنشاء قائمة بعدد الكلمات

وحفظها في Dashboard_path
+
قاعدة البيانات

python3 core8/pwb.py mdcount/words newpages
python3 core8/pwb.py mdcount/words
python3 core8/pwb.py mdcount/words listnew

python3 core8/pwb.py mdcount/words more400

python3 core8/pwb.py mdcount/words less100
python3 core8/pwb.py mdcount/words sql

"""

import os
import sys

from apis import mdwiki_api
from newapi import printe
from mdcount.bots.links import get_links_from_cats
from mdapi_sql import sql_for_mdwiki
from mdcount.ref_words_bot import get_jsons, logaa, make_old_values, do_to_sql
from mdcount.bots import lead
# ---
if os.getenv("HOME"):
    Dashboard_path = os.getenv("HOME") + "/public_html/td"
else:
    Dashboard_path = "I:/mdwiki/mdwiki/public_html/td"
# ---
all_tab_data = {1: {}}
lead_tab_data = {1: {}}
# ---
file_all = f"{Dashboard_path}/Tables/jsons/allwords.json"
file_lead = f"{Dashboard_path}/Tables/jsons/words.json"


def start_to_sql():
    return do_to_sql(all_tab_data[1], lead_tab_data[1], ty="word")


def count_words(title):
    # ---
    text = mdwiki_api.GetPageText(title)
    # ---
    lead_c, all_c = lead.count_all(title='', text=text)
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
    all_tab_data[1], lead_tab_data[1] = get_jsons(file_all, file_lead, "word")
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
        count_words(x)
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
    # python3 core8/pwb.py mdcount/words test
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
