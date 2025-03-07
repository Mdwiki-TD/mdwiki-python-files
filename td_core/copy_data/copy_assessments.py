#!/usr/bin/python3
"""

python3 core8/pwb.py mdcount/bots/copy_assessments

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
que = '''select DISTINCT title, importance from assessments;'''
# ---
NEW_DATA_duplicate = {}
NEW_DATA = {}
# ---
with open(f'{project_tables}/assessments.json', "r", encoding="utf-8") as f:
    data_in_json = json.load(f)
# ---
data_in_json = {x.strip() : data_in_json[x] for x in data_in_json}
# ---
for x, numb in data_in_json.items():
    NEW_DATA[x] = numb
# ---
print(f"{len(NEW_DATA)=}, {len(NEW_DATA_duplicate)=}")
# ---
in_sql = {}
# ---
for q in sql_for_mdwiki.select_md_sql(que, return_dict=True):
    title = q['title']
    if not NEW_DATA.get(title):
        in_sql[title] = q['importance']
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

DROP TABLE IF EXISTS `assessments`;
CREATE TABLE `assessments` (
  `id` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(120) NOT NULL,
  `importance` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `assessments` (`id`, `title`, `importance`) VALUES
'''
# ---
n = 0
# ---
lines = []
# ---
# sort NEW_DATA by importance
NEW_DATA = {k: v for k, v in sorted(NEW_DATA.items(), key=lambda item: item[1])}
# ---
len_empty = len([x for x in NEW_DATA.values() if not x])
# ---
print(f"{len(NEW_DATA)=}, {len_empty=}")
# ---
for title, importance in NEW_DATA.items():
    n += 1
    # ---
    title = escape_string(title)
    # ---
    if importance.lower() in ["unknown", "na"]:
        importance = ""
    # ---
    line = f"({n},	'{title}',	'{importance}')"
    # ---
    lines.append(line)
# ---
text += ",\n".join(lines)
text += ";"
# ---
with open(f'{Dir}/assessments.txt', "w", encoding="utf-8") as f:
    f.write(text)
