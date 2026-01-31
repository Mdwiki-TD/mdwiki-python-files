#!/usr/bin/python3
"""

إنشاء قائمة بعدد المراجع والكلمات

وحفظها في Dashboard_path
+
قاعدة البيانات


python3 core8/pwb.py mdcount/countrefs_and_words merge
python3 core8/pwb.py mdcount/countrefs_and_words newpages

python3 core8/pwb.py mdcount/countrefs_and_words -title:Esophageal_rupture

"""

import json
import os
import sys

from apis import mdwiki_api
from mdapi_sql import sql_for_mdwiki
from mdcount.bots import lead
from mdcount.bots.countref_bots import count_ref_from_text
from mdcount.bots.links import get_links_from_cats
from mdcount.ref_words_bot import do_to_sql, get_jsons_new, logaa, make_old_values
from newapi import printe

# ---
if os.getenv("HOME"):
    Dashboard_path = os.getenv("HOME") + "/public_html/td"
else:
    Dashboard_path = "I:/mdwiki/mdwiki/public_html/td"
# ---
refs_tab_data = {"all": {}, "lead": {}}
words_tab_data = {"all": {}, "lead": {}}
# ---
file_all_refs = f"{Dashboard_path}/Tables/jsons/all_refcount.json"
file_lead_refs = f"{Dashboard_path}/Tables/jsons/lead_refcount.json"
# ---
file_all_words = f"{Dashboard_path}/Tables/jsons/allwords.json"
file_lead_words = f"{Dashboard_path}/Tables/jsons/words.json"


def start_to_sql():
    do_to_sql(words_tab_data["all"], words_tab_data["lead"], ty="word")
    do_to_sql(refs_tab_data["all"], refs_tab_data["lead"], ty="ref")


def count_words(title, text):
    # ---
    lead_c, all_c = lead.count_all(title="", text=text)
    # ---
    words_tab_data["all"][title] = all_c
    words_tab_data["lead"][title] = lead_c
    # ---
    printe.output(f"<<green>> all:{all_c} \t lead:{lead_c}")


def count_refs(title, text):
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
    refs_tab_data["all"][title] = all_c
    refs_tab_data["lead"][title] = lead_c
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


def get_links(ty="ref"):
    # ---
    titles = []
    # ---
    if ty == "word":
        old_values = make_old_values(words_tab_data["all"], words_tab_data["lead"])
    else:
        old_values = make_old_values(refs_tab_data["all"], refs_tab_data["lead"])
    # ---
    if "sql" in sys.argv:
        titles = from_sql(old_values)
    else:
        titles = get_links_from_cats()
    # ---
    if "newpages" in sys.argv:
        titles = [x for x in titles if (x not in old_values)]
    # ---
    return titles


def main():
    # ---
    words_tab_data["all"], words_tab_data["lead"] = get_jsons_new(file_all_words, file_lead_words, "word")
    # ---
    refs_tab_data["all"], refs_tab_data["lead"] = get_jsons_new(file_all_refs, file_lead_refs, "ref")
    # ---
    if "merge" in sys.argv:
        # ---
        with open(file_all_words, "w", encoding="utf-8") as outfile:
            printe.output(f"<<green>> {len(words_tab_data['all'])} lines to {file_all_words}")
            json.dump(words_tab_data["all"], outfile, sort_keys=True, indent=2)
        # ---
        with open(file_lead_words, "w", encoding="utf-8") as outfile:
            printe.output(f"<<green>> {len(words_tab_data['lead'])} lines to {file_lead_words}")
            json.dump(words_tab_data["lead"], outfile, sort_keys=True, indent=2)
        # ---
        with open(file_all_refs, "w", encoding="utf-8") as outfile:
            printe.output(f"<<green>> {len(refs_tab_data['all'])} lines to {file_all_refs}")
            json.dump(refs_tab_data["all"], outfile, sort_keys=True, indent=2)
        # ---
        with open(file_lead_refs, "w", encoding="utf-8") as outfile:
            printe.output(f"<<green>> {len(refs_tab_data['lead'])} lines to {file_lead_refs}")
            json.dump(refs_tab_data["lead"], outfile, sort_keys=True, indent=2)
        # ---
        start_to_sql()
        # ---
        exit()
    # ---
    limit = 100 if "limit100" in sys.argv else 10000
    # ---
    # python3 core8/pwb.py mdcount/countref -title:Testosterone_\(medication\)
    # ---
    vaild_links = []
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        # ---
        if arg == "-title":
            vaild_links = [value.replace("_", " ")]
    # ---
    if not vaild_links:
        vaild_links = get_links()
    # ---
    for numb, x in enumerate(vaild_links):
        # ---
        x = x.replace("\\'", "'")
        # ---
        printe.output("------------------")
        printe.output(f"page {numb} from {len(vaild_links)}, x:{x}")
        # ---
        if numb >= limit:
            break
        # ---
        text = mdwiki_api.GetPageText(x)
        # ---
        count_words(x, text)
        count_refs(x, text)
        # ---
        # if numb == 10 or str(numb).endswith("00"):
        #     logaa(file_lead_words, words_tab_data["lead"])
        #     logaa(file_all_words, words_tab_data["all"])
        #     logaa(file_lead_refs, refs_tab_data["lead"])
        #     logaa(file_all_refs, refs_tab_data["all"])
    # ---
    logaa(file_lead_words, words_tab_data["lead"])
    logaa(file_all_words, words_tab_data["all"])
    # ---
    logaa(file_lead_refs, refs_tab_data["lead"])
    logaa(file_all_refs, refs_tab_data["all"])
    # ---
    start_to_sql()


def test():
    # python3 core8/pwb.py mdcount/countref test
    # ---
    refs_tab_data["lead"]["Yemen1"] = 50
    refs_tab_data["all"]["Yemen1"] = 50
    # ---
    refs_tab_data["lead"]["Sana'a"] = 500
    refs_tab_data["all"]["Sana'a"] = 100
    # ---
    words_tab_data["lead"]["Yemen1"] = 50
    words_tab_data["all"]["Yemen1"] = 50
    # ---
    words_tab_data["lead"]["Sana'a"] = 500
    words_tab_data["all"]["Sana'a"] = 100
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
        sys.argv.append("sql")
        # ---
        main()
