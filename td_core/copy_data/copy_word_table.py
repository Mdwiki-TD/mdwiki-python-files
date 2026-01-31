#!/usr/bin/python3
"""

python3 core8/pwb.py mdcount/bots/copy_word_table

"""
from pymysql.converters import escape_string
import json
import logging

# ---
import os
import sys
from pathlib import Path

# ---
from mdapi_sql import sql_for_mdwiki

logger = logging.getLogger(__name__)

# ---
Dir = str(Path(__file__).parents[0])
# ---
if os.getenv("HOME"):
    public_html_dir = os.getenv("HOME") + "/public_html"
else:
    public_html_dir = "I:/mdwiki/mdwiki/public_html"
# ---
project_tables = Path(public_html_dir) / "td/Tables/jsons"
# ---
que = """select DISTINCT w_title, w_lead_words, w_all_words from words;"""
# ---
in_sql_lead = {}
in_sql_all = {}
# ---
for q in sql_for_mdwiki.select_md_sql(que, return_dict=True):
    # ---
    w_title = q["w_title"]
    w_lead_words = q["w_lead_words"]
    w_all_words = q["w_all_words"]
    # ---
    in_sql_lead[w_title] = w_lead_words
    in_sql_all[w_title] = w_all_words
# ---
with open(f"{project_tables}/words.json", "r", encoding="utf-8") as f:
    lead_words = json.load(f)

with open(f"{project_tables}/allwords.json", "r", encoding="utf-8") as f:
    all_words = json.load(f)
# ---
new_words = {}
# ---
na_list = list(all_words.keys())
# ---
for x in lead_words.keys():
    if x not in na_list:
        na_list.append(x)
# ---
# remove duplicates from list
# na_list = list(set(na_list))
# ---
len_all = len(na_list)
# ---
UPDATE = []
INSERT = []
same = 0
# ---
for tit in na_list:
    # ---
    tit = tit.strip()
    # ---
    lead = lead_words.get(tit, 0)
    All = all_words.get(tit, 0)
    # ---
    sql_lead = in_sql_lead.get(tit)
    sql_all = in_sql_all.get(tit)
    # ---
    title2 = escape_string(tit)
    # ---
    if tit not in in_sql_lead:
        INSERT.append([lead, All, tit])
    elif sql_lead == lead and sql_all == All:
        same += 1
    else:
        if lead > 10 and All > 10:
            UPDATE.append([lead, All, tit])
all_textx = []
texts = []
# ---
n = 0
# ---
print("----------------")
printe.output("<<yellow>> UPDATE: ")
# ---
if UPDATE:
    if "update" in sys.argv:
        for tab in UPDATE:
            # ---
            lead, All, tit = tab
            # ---
            # title2 = escape_string(tit)
            # ---
            title2 = tit
            # ---
            if title2.find("'") != -1:
                title2 = f'"{title2}"'
            else:
                title2 = f"'{title2}'"
            # ---
            update_qua = """UPDATE words SET w_lead_words = %s, w_all_words = %s WHERE w_title = %s;"""
            values = [lead, All, tit]
            # ---
            qu = f"""UPDATE words SET w_lead_words = {lead}, w_all_words = {All} WHERE w_title = {title2};"""
            # ---
            n += 1
            # ---
            all_textx.append(qu)
            texts.append(qu)
            # ---
            values = []
            # ---
            if len(texts) % 50 == 0 or n == len(UPDATE):
                tt = "\n".join(texts)
                # ---
                printe.output("====")
                printe.output(f"{n} run sql for {len(texts)} lines.")
                # ---
                printe.output(tt)
                # ---
                vfg = sql_for_mdwiki.mdwiki_sql(tt, values=values)
                # ---
                texts = []
                # ---
                if "break" in sys.argv:
                    break
    else:
        printe.output('add "update" to sys.argv to update new words.')
        printe.output(f"{len(UPDATE)=}")
        printe.output(UPDATE[0])
# ---
print("----------------")
printe.output("<<yellow>> INSERT: ")
# ---
if INSERT != []:
    # ---
    intert_quas = [f"""('{title2}', {lead}, {All})""" for lead, All, title2 in INSERT]
    # ---
    insert_line = ",\n".join(INSERT)
    if "insert" in sys.argv:
        # ---
        qu = "INSERT INTO words (w_title, w_lead_words, w_all_words) values\n" + insert_line
        printe.output(qu)
        vfg = sql_for_mdwiki.mdwiki_sql(qu, update=True)
    else:
        printe.output('add "insert" to sys.argv to insert new words.')
        printe.output(f"{len(INSERT)=}")
        printe.output(insert_line[0])
# ---
print("----------------")
# ---
printe.output(f"len lead_words from file: {len(lead_words)}")
printe.output(f"len all_words from file: {len(all_words)}")
# ---
printe.output(f"len sql titles: {len(in_sql_lead)}")
printe.output(f"pages with same values in sql and file: {same}")
# ---
with open(f"{Dir}/words.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(all_textx))
