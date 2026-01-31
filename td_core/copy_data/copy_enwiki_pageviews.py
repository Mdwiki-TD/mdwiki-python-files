#!/usr/bin/python3
"""

python3 core8/pwb.py copy_data/copy_enwiki_pageviews

"""
import json

# ---
import os
from pathlib import Path

# ---
from mdapi_sql import sql_for_mdwiki
from pymysql.converters import escape_string

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
NEW_DATA_duplicate = {}
NEW_DATA = {}
# ---
with open(f"{project_tables}/enwiki_pageviews.json", "r", encoding="utf-8") as f:
    data_in_json = json.load(f)
# ---
data_in_json = {x.strip(): data_in_json[x] for x in data_in_json}
# ---
for x, numb in data_in_json.items():
    NEW_DATA[x] = numb
# ---
logger.info(f"{len(NEW_DATA)=}, {len(NEW_DATA_duplicate)=}")
# ---
in_sql = {}
# ---
que = """select DISTINCT title, en_views from enwiki_pageviews;"""
# ---
for q in sql_for_mdwiki.select_md_sql(que, return_dict=True):
    title = q["title"]
    if not NEW_DATA.get(title):
        in_sql[title] = q["en_views"]
# ---
logger.info(f"{len(in_sql)=}")
logger.info(in_sql)
# ---
NEW_DATA.update(in_sql)
# ---
text = """
-- Adminer 4.8.1 MySQL 5.5.5-10.6.20-MariaDB-log dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `enwiki_pageviews`;
CREATE TABLE `enwiki_pageviews` (
  `id` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(120) NOT NULL,
  `en_views` int(6) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `enwiki_pageviews` (`id`, `title`, `en_views`) VALUES
"""
# ---
n = 0
# ---
lines = []
# ---
# sort NEW_DATA by keys
NEW_DATA = {k: v for k, v in sorted(NEW_DATA.items(), key=lambda item: item[0])}
# ---
len_empty = len([x for x in NEW_DATA.values() if x == 0])
# ---
logger.info(f"{len(NEW_DATA)=}, {len_empty=}")
# ---
for title, en_views in NEW_DATA.items():
    n += 1
    # ---
    title = escape_string(title)
    # ---
    line = f"({n},	'{title}',	{en_views})"
    # ---
    lines.append(line)
# ---
text += ",\n".join(lines)
text += ";"
# ---
with open(f"{Dir}/enwiki_pageviews.txt", "w", encoding="utf-8") as f:
    f.write(text)
