#!/usr/bin/python3
"""

python3 core8/pwb.py copy_data/by_title/exists_db


"""

import json
import logging
import os
import sys

import tqdm

# ---
from mdapi_sql import sql_for_mdwiki_new
from mdpyget.bots.to_sql import insert_dict

logger = logging.getLogger(__name__)

if os.getenv("HOME"):
    Dashboard_path = os.getenv("HOME") + "/public_html/td"
else:
    Dashboard_path = "I:/mdwiki/mdwiki/public_html/td"
# ---
cash_exists = Dashboard_path + "/Tables/cash_exists"
json_files = [f for f in os.listdir(cash_exists) if f.endswith(".json")]

que = """select DISTINCT article_id, code from all_exists;"""
# ---
in_sql = {}
# ---
for q in sql_for_mdwiki_new.select_md_sql(que, return_dict=True):
    title = q["article_id"]
    code = q["code"]
    # ---
    if code in in_sql:
        in_sql[code].append(title)
    else:
        in_sql[code] = [title]


def to_sql_d(titles_data):
    # ---
    new_all = {}
    # ---
    for lang_code, titles in tqdm.tqdm(titles_data.items()):
        same = 0
        # ---
        to_add = []
        # ---
        is_in = in_sql.get(lang_code, [])
        # ---
        for title in titles:
            # ---
            if title.strip():
                # ---
                if title in is_in:
                    same += 1
                else:
                    to_add.append(title)
        # ---
        in_sql_not_in_new = [x for x in is_in if x not in titles]
        # ---
        # printe.output(f"<<red>> {lang_code}: {same=}, {len(to_add)=}), {len(in_sql_not_in_new)=}")
        # ---
        if to_add:
            new_all[lang_code] = to_add
    # ---
    printe.output(f"<<green>> all langs: {len(new_all)}")
    # ---
    for lang_code, to_add in new_all.items():
        # ---
        printe.output(f"________\n<<yellow>> {lang_code}: {len(to_add)=}:")
        # ---
        new_data = [{"article_id": title, "code": lang_code} for title in to_add]
        # ---
        insert_dict(new_data, "all_exists", ["article_id", "code"], lento=1000, title_column="article_id")


def main():
    # ---
    langs = list(set([x.replace(".json", "") for x in json_files]))
    # ---
    data_all = {}
    # ---
    for lang_code in tqdm.tqdm(langs):
        # ---
        file_name = cash_exists + "/" + lang_code + ".json"
        # ---
        data = []
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
        # ---
        data = list(set(data))
        # ---
        data_all[lang_code] = data
    # ---
    to_sql_d(data_all)
    # break


def test():
    # python3 core8/pwb.py copy_data/exists_db test
    # ---
    data = {"ar": ["Asbestosis", "RTT", "Zoster vaccine"]}
    # ---
    to_sql_d(data)


if __name__ == "__main__":
    # ---
    if "test" in sys.argv:
        test()
        exit()
    # ---
    main()
