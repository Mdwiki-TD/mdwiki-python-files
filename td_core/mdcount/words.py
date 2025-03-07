#!/usr/bin/python3
"""

إنشاء قائمة بعدد الكلمات
python3 core8/pwb.py mdcount/words newpages
python3 core8/pwb.py mdcount/words
python3 core8/pwb.py mdcount/words listnew

python3 core8/pwb.py mdcount/words more400

python3 core8/pwb.py mdcount/words less100
python3 core8/pwb.py mdcount/words sql

"""

import os
import json

import sys

# ---
from apis import mdwiki_api
from newapi import printe
from mdcount.bots.links import get_valid_Links
from mdcount.bots import lead
from mdpyget.bots.to_sql import to_sql

if os.getenv("HOME"):
    Dashboard_path = os.getenv("HOME") + "/public_html/td"
else:
    Dashboard_path = "I:/mdwiki/mdwiki/public_html/td"
# ---
json_file = {}
# ---
lead_words = {}
# ---
all_words_n = {}


def get_word_files():
    # ---
    global json_file, lead_words, all_words_n
    # ---
    json_file[1] = f'{Dashboard_path}/Tables/jsons/allwords.json'
    # ---
    all_words_n = {}
    # ---
    with open(json_file[1], "r", encoding="utf-8") as f:
        all_words_n = json.load(f)
    # ---
    json_file[0] = f'{Dashboard_path}/Tables/jsons/words.json'
    # ---
    lead_words = {}
    # ---
    with open(json_file[0], "r", encoding="utf-8") as f:
        lead_words = json.load(f)
    # ---
    printe.output(f'len of lead_words:{len(lead_words.keys())}')

    # ---


# ---
get_word_files()


def log(file, table):
    with open(file, "w", encoding="utf-8") as aa:
        json.dump(table, aa, sort_keys=True)
    # ---
    printe.output(f'<<green>> {len(table)} lines to {file}')


# ---
Nore = {1: False}
for arg in sys.argv:
    if arg in ['new', 'listnew', 'less100', 'more400']:
        Nore[1] = True


def mmain():
    # ---
    n = 0
    limit = 100 if 'limit100' in sys.argv else 10000
    # ---
    vaild_links = get_valid_Links(lead_words)
    # ---
    kkk = {1: vaild_links}
    # ---
    for x in kkk[1]:
        # ---
        x = x.replace("\\'", "'")
        # ---
        n += 1
        # ---
        printe.output('------------------')
        printe.output('page %d from %d, x:%s' % (n, len(kkk[1]), x))
        # ---
        if n >= limit:
            break
        # ---
        text = mdwiki_api.GetPageText(x)
        # ---
        # pageword = mdwiki_api.wordcount(x)
        # leadword = lead.count_lead(x)
        leadword, pageword = lead.count_all(title='', text=text)
        # ---
        printe.output(f'\t\t pageword:{pageword}')
        printe.output(f'\t\t leadword:{leadword}')
        # ---
        all_words_n[x] = pageword
        lead_words[x] = leadword
        # ---
        if n == 10 or str(n).endswith('00'):
            log(json_file[0], lead_words)
            log(json_file[1], all_words_n)
    # ---
    log(json_file[0], lead_words)
    log(json_file[1], all_words_n)
    # ---
    start_to_sql()


def start_to_sql():
    data2 = [{"w_title": x, "w_lead_words": v, "w_all_words": all_words_n.get(x, 0)} for x, v in lead_words.items()]
    # ---
    to_sql(data2, "words", ["w_title", "w_lead_words", "w_all_words"], title_column="w_title")


def test():
    # python3 core8/pwb.py mdcount/words test
    # ---
    lead_words["Yemenz"] = 50
    all_words_n["Yemen1"] = 50
    # ---
    lead_words["Sana'xa"] = 500
    all_words_n["Sana'x1a"] = 100
    # ---
    start_to_sql()


if __name__ == "__main__":
    # ---
    if "test" in sys.argv:
        test()
        exit()
    # ---
    mmain()
    # ---
    if "sql" not in sys.argv:
        sys.argv.append('sql')
        # ---
        mmain()
