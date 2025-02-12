#!/usr/bin/python3
"""

python3 core8/pwb.py mdcount/copy_word_table

"""

#
# (C) Ibrahem Qasim, 2022
#
#
# ---
import json
import sys
from pathlib import Path

# ---
from mdapi_sql import sql_for_mdwiki
from newapi import printe
from pymysql.converters import escape_string

# ---
Dir = str(Path(__file__).parents[0])
# print(f'Dir : {Dir}')
# split path before "mdwiki"
dir2 = Dir.replace('\\', '/')
dir2 = dir2.split('/bybot/')[0]
# ---
que = '''select DISTINCT w_title, w_lead_words, w_all_words from words;'''
# ---
in_sql_lead = {}
in_sql_all = {}
# ---
for q in sql_for_mdwiki.select_md_sql(que, return_dict=True):
    # ---
    w_title = q['w_title']
    w_lead_words = q['w_lead_words']
    w_all_words = q['w_all_words']
    # ---
    in_sql_lead[w_title] = w_lead_words
    in_sql_all[w_title] = w_all_words
# ---
project_tables = Path(dir2) / 'public_html' / 'td' / 'Tables'
# ---
with open(f'{project_tables}/words.json', "r", encoding="utf-8") as f:
    lead_words = json.load(f)

with open(f'{project_tables}/allwords.json', "r", encoding="utf-8") as f:
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
    qua = f"""INSERT INTO words (w_title, w_lead_words, w_all_words) SELECT '{title2}', {lead}, {All}
    WHERE NOT EXISTS ( SELECT 1 FROM words  WHERE w_title = {title2} );

    UPDATE words SET w_lead_words = {lead}, w_all_words = {All} WHERE w_title = '{title2}';
    """
    # ---
    qua_update = f"""UPDATE words SET w_lead_words = {lead}, w_all_words = {All} WHERE w_title = '{title2}';"""
    # ---
    if tit not in in_sql_lead:
        qua_new = f"""('{title2}', {lead}, {All})"""
        # ---
        INSERT.append(qua_new)
    elif sql_lead == lead and sql_all == All:
        same += 1
    else:
        if lead > 10 and All > 10:
            UPDATE.append(qua_update)
all_textx = []
texts = []
# ---
n = 0
# ---
print("----------------")
printe.output("<<yellow>> UPDATE: ")
# ---
if UPDATE != []:
    if 'update' in sys.argv:
        for qu in UPDATE:
            # ---
            n += 1
            # ---
            all_textx.append(qu)
            texts.append(qu)
            # ---
            if len(texts) % 50 == 0 or n == len(UPDATE):
                tt = "\n".join(texts)
                # ---
                printe.output('====')
                printe.output(f'{n} run sql for {len(texts)} lines.')
                # ---
                printe.output(tt)
                # ---
                vfg = sql_for_mdwiki.mdwiki_sql(tt, update=True)
                # ---
                texts = []
                # ---
                if 'break' in sys.argv:
                    break
    else:
        printe.output('add "update" to sys.argv to update new words.')
        printe.output(f'{len(UPDATE)=}')
        printe.output(UPDATE[0])
# ---
print("----------------")
printe.output("<<yellow>> INSERT: ")
# ---
if INSERT != []:
    insert_line = ',\n'.join(INSERT)
    if 'insert' in sys.argv:
        # ---
        qu = 'INSERT INTO words (w_title, w_lead_words, w_all_words) values\n' + insert_line
        printe.output(qu)
        vfg = sql_for_mdwiki.mdwiki_sql(qu, update=True)
    else:
        printe.output('add "insert" to sys.argv to insert new words.')
        printe.output(f'{len(INSERT)=}')
        printe.output(insert_line[0])
# ---
print("----------------")
# ---
printe.output(f'len lead_words from file: {len(lead_words)}')
printe.output(f'len all_words from file: {len(all_words)}')
# ---
printe.output(f'len sql titles: {len(in_sql_lead)}')
printe.output(f'pages with same values in sql and file: {same}')
# ---
with open(f'{Dir}/words.txt', "w", encoding="utf-8") as f:
    f.write("\n".join(all_textx))
