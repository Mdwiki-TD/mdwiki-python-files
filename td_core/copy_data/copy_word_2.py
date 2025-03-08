#!/usr/bin/python3
"""

python3 core8/pwb.py mdcount/bots/copy_word_2

"""
# ---
import os
import json
import sys
from pathlib import Path
from pymysql.converters import escape_string
# ---
from mdapi_sql import sql_for_mdwiki
from newapi import printe

# ---
Dir = str(Path(__file__).parents[0])
# ---
if os.getenv("HOME"):
    public_html_dir = os.getenv("HOME") + "/public_html"
else:
    public_html_dir = "I:/mdwiki/mdwiki/public_html"
# ---
project_tables = Path(public_html_dir) / 'td/Tables/jsons'
# ---
que = '''select DISTINCT w_title, w_lead_words, w_all_words from words;'''
# ---
NEW_DATA_duplicate = {}
NEW_DATA = {}
# ---
with open(f'{project_tables}/words.json', "r", encoding="utf-8") as f:
    lead_words = json.load(f)

with open(f'{project_tables}/allwords.json', "r", encoding="utf-8") as f:
    all_words = json.load(f)
# ---
lead_words = {x.strip() : lead_words[x] for x in lead_words}
all_words = {x.strip() : all_words[x] for x in all_words}
# ---
for x, numb in lead_words.items():
    NEW_DATA[x] = {'lead' : numb, 'all' : all_words.get(x, 0)}
# ---
for x3, numb2 in all_words.items():
    if x3 not in NEW_DATA:
        NEW_DATA[x3] = {'lead' : lead_words.get(x3, 0), 'all' : numb2}
    elif numb2 != NEW_DATA[x3]['all']:
        NEW_DATA_duplicate[x3] = {'lead' : lead_words.get(x3, 0), 'all' : numb2}
# ---
print(f"{len(NEW_DATA)=}, {len(NEW_DATA_duplicate)=}")
# ---
in_sql = {}
# ---
for q in sql_for_mdwiki.select_md_sql(que, return_dict=True):
    w_title = q['w_title']
    if not NEW_DATA.get(w_title):
        in_sql[w_title] = {'lead' : q['w_lead_words'], 'all' : q['w_all_words']}
# ---
print(f"{len(in_sql)=}")
print(in_sql)
# ---
NEW_DATA.update(in_sql)
# ---
text = '''
-- Adminer 4.8.1 MySQL 5.5.5-10.6.20-MariaDB-log dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `words`;
CREATE TABLE `words` (
  `w_id` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `w_title` varchar(120) NOT NULL,
  `w_lead_words` int(6) DEFAULT NULL,
  `w_all_words` int(6) DEFAULT NULL,
  PRIMARY KEY (`w_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `words` (`w_id`, `w_title`, `w_lead_words`, `w_all_words`) VALUES
'''
# (1,	'Second-degree atrioventricular block',	278,	1267),
# ---
n = 0
# ---
lines = []
# ---
for title, tab in NEW_DATA.items():
    n += 1
    # ---
    title = escape_string(title)
    # ---
    line = f"({n},	'{title}',	{tab['lead']},	{tab['all']})"
    # ---
    lines.append(line)
# ---
text += ",\n".join(lines)
text += ";"
# ---
with open(f'{Dir}/words.txt', "w", encoding="utf-8") as f:
    f.write(text)
