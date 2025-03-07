#!/usr/bin/python3
"""

python3 core8/pwb.py mdcount/bots/copy_refs_2

"""
# ---
import os
import json
from pathlib import Path
from pymysql.converters import escape_string
# ---
from mdapi_sql import sql_for_mdwiki

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
que = '''select DISTINCT r_title, r_lead_refs, r_all_refs from refs_counts;'''
# ---
NEW_DATA_duplicate = {}
NEW_DATA = {}
# ---
with open(f'{project_tables}/lead_refcount.json', "r", encoding="utf-8") as f:
    lead_refs = json.load(f)

with open(f'{project_tables}/all_refcount.json', "r", encoding="utf-8") as f:
    all_refs = json.load(f)
# ---
lead_refs = {x.strip() : lead_refs[x] for x in lead_refs}
all_refs = {x.strip() : all_refs[x] for x in all_refs}
# ---
for x, numb in lead_refs.items():
    NEW_DATA[x] = {'lead' : numb, 'all' : all_refs.get(x, 0)}
# ---
for x3, numb2 in all_refs.items():
    if x3 not in NEW_DATA:
        NEW_DATA[x3] = {'lead' : lead_refs.get(x3, 0), 'all' : numb2}
    elif numb2 != NEW_DATA[x3]['all']:
        NEW_DATA_duplicate[x3] = {'lead' : lead_refs.get(x3, 0), 'all' : numb2}
# ---
print(f"{len(NEW_DATA)=}, {len(NEW_DATA_duplicate)=}")
# ---
in_sql = {}
# ---
for q in sql_for_mdwiki.select_md_sql(que, return_dict=True):
    r_title = q['r_title']
    if not NEW_DATA.get(r_title):
        in_sql[r_title] = {'lead' : q['r_lead_refs'], 'all' : q['r_all_refs']}
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

DROP TABLE IF EXISTS `refs_counts`;
CREATE TABLE `refs_counts` (
  `r_id` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `r_title` varchar(120) NOT NULL,
  `r_lead_refs` int(6) DEFAULT NULL,
  `r_all_refs` int(6) DEFAULT NULL,
  PRIMARY KEY (`r_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `refs_counts` (`r_id`, `r_title`, `r_lead_refs`, `r_all_refs`) VALUES
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
with open(f'{Dir}/refs_counts.txt', "w", encoding="utf-8") as f:
    f.write(text)
