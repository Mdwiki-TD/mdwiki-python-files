"""

python3 core8/pwb.py mass/radio/lists/cases_to_cats

from mass.radio.lists.cases_to_cats import cases_cats# cases_cats()
"""
import json
import re
import os
from pathlib import Path
from datetime import datetime
from newapi.ncc_page import CatDepth
from newapi import printe
# ---
main_dir = Path(__file__).parent.parent
# ---
cases_cats_file = main_dir / 'jsons/cases_cats.json'
# ---
cases_cats_list = []
# ---
if not os.path.exists(cases_cats_file):
    with open(cases_cats_file, 'w', encoding='utf-8') as f:
        json.dump(cases_cats_list, f)
# ---
with open(cases_cats_file, 'r', encoding='utf-8') as f:
    cases_cats_list = json.load(f)
# ---
def new_list():
    members = CatDepth("Category:Radiopaedia images by case", sitecode="www", family="nccommons", depth=0, ns="14")
    reg = r"^Category:Radiopaedia case (\d+) (.*?)$"
    # ---
    id2cat = {}
    # ---
    for cat in members:
        match = re.match(reg, cat)
        if match:
            case_id = match.group(1)
            # ---
            id2cat[case_id] = cat
    # ---
    print(f"cases_cats, lenth of members: {len(members)}, lenth of id2cat: {len(id2cat)} ")
    # ---
    with open(cases_cats_file, 'w', encoding='utf-8') as f:
        json.dump(id2cat, f)
    # ---
    return id2cat

def cases_cats():
    global cases_cats_list

    # Get the time of last modification
    last_modified_time = os.path.getmtime(cases_cats_file)
    # ---
    date = datetime.fromtimestamp(last_modified_time).strftime('%Y-%m-%d')
    # ---
    today = datetime.today().strftime('%Y-%m-%d')
    # ---
    if date != today or not cases_cats_list:
        printe.output(f"<<purple>> last modified: {date} , today: {today}, len: {len(cases_cats_list)} ")
        cases_cats_list = new_list()
    # ---
    return cases_cats_list

if "__main__" == __name__:
    cases_cats()