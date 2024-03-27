#!/usr/bin/python3
"""

(missing_in_enwiki|medwiki_to_enwiki|sames)\.json

Usage:

# python3 core8/pwb.py mdpages/get_md_to_en nodump
# python3 core8/pwb.py mdpages/get_md_to_en -others
# python3 core8/pwb.py mdpages/get_md_to_en -others nodump

"""
import json
import sys

# ---
from mdpy.bots import sql_for_mdwiki
from mdpy.bots import sql_qids_others
from mdpy import printe
from mdpy.bots import catdepth2
from mdpy.bots import wiki_api
from mdpy.bots import mdwiki_api
from mdpy.bots.check_title import valid_title  # valid_title(title)
from mdpages import qids_help
# ---
from pathlib import Path

Dir = str(Path(__file__).parents[0])
# print(f'Dir : {Dir}')
# ---
dir2 = Dir.replace("\\", "/")
dir2 = dir2.split("/mdwiki/")[0] + "/mdwiki"
# ---
dir2 += "/public_html/Translation_Dashboard/Tables/"
# ---
json_ext = "_other.json" if "-others" in sys.argv else ".json"

# ---
# qids_help.get_o_qids_new(o_qids, t_qids_in)
# qids_help.get_pages_to_work(ty="td|other")
# qids_help.check(work_list, all_pages)
# ---
def start():
    ty = "other" if "-others" in sys.argv else "td"
    # ---
    to_work, all_pages = qids_help.get_pages_to_work(ty)
    # ---
    qids_help.check(to_work, all_pages)


if __name__ == "__main__":
    start()
