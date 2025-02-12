#!/usr/bin/python3
"""

إنشاء قائمة بعدد الكلمات

python3 core8/pwb.py mdcount/words
python3 core8/pwb.py mdcount/words listnew

python3 core8/pwb.py mdcount/words more400

python3 core8/pwb.py mdcount/words less100
python3 core8/pwb.py mdcount/words sql

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import os
import json

import sys

# ---
from apis import mdwiki_api
from newapi import printe
from mdcount.links import get_valid_Links
from mdcount import lead

if os.getenv("HOME"):
    public_html_dir = os.getenv("HOME") + "/public_html"
else:
    public_html_dir = "I:/mdwiki/mdwiki/public_html"
# ---
json_file = {}
# ---
words_n = {}
# ---
all_words_n = {}


def get_word_files():
    # ---
    global json_file, words_n, all_words_n
    # ---
    json_file[1] = f'{public_html_dir}/td/Tables/jsons/allwords.json'
    # ---
    all_words_n = {}
    # ---
    with open(json_file[1], "r", encoding="utf-8") as f:
        all_words_n = json.load(f)
    # ---
    json_file[0] = f'{public_html_dir}/td/Tables/jsons/words.json'
    # ---
    words_n = {}
    # ---
    with open(json_file[0], "r", encoding="utf-8") as f:
        words_n = json.load(f)
    # ---
    printe.output(f'len of words_n:{len(words_n.keys())}')

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
    vaild_links = get_valid_Links(words_n)
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
        words_n[x] = leadword
        # ---
        if n == 10 or str(n).endswith('00'):
            log(json_file[0], words_n)
            log(json_file[1], all_words_n)
        # ---
    # ---
    log(json_file[0], words_n)
    log(json_file[1], all_words_n)


# ---
if __name__ == '__main__':
    mmain()
    # ---
    if "sql" not in sys.argv:
        sys.argv.append('sql')
        # ---
        mmain()
# ---
