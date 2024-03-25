"""

Usage:
from mass.radio.lists.PD_medical import PD_medical_pages_def
PD_medical_pages = PD_medical_pages_def()

"""

import json
import os
from datetime import datetime
from pathlib import Path

from newapi import printe
from newapi.ncc_page import CatDepth

# ---
main_dir = Path(__file__).parent.parent
# ---
pd_file = main_dir / "jsons/PD_medical_pages.json"
# ---
PD_medical_pages = []
# ---
if not os.path.exists(pd_file):
    with open(pd_file, "w", encoding="utf-8") as f:
        json.dump(PD_medical_pages, f)
# ---
with open(pd_file, encoding="utf-8") as f:
    PD_medical_pages = json.load(f)


# ---
def new_list():
    members = CatDepth("Category:PD medical",
                       sitecode="www",
                       family="nccommons",
                       depth=1,
                       ns="10")
    # ---
    print(f"lenth of members: {len(members)} ")
    # ---
    with open(pd_file, "w", encoding="utf-8") as f:
        json.dump(PD_medical_pages, f)
    # ---
    return members


def PD_medical_pages_def():
    global PD_medical_pages
    return PD_medical_pages

    # Get the time of last modification
    last_modified_time = os.path.getmtime(pd_file)
    # ---
    date = datetime.fromtimestamp(last_modified_time).strftime("%Y-%m-%d")
    # ---
    today = datetime.today().strftime("%Y-%m-%d")
    # ---
    if date != today or not PD_medical_pages:
        printe.output(
            f"<<purple>> PD medical pages last modified: {date}, today: {today}, current length: {len(PD_medical_pages)}"
        )
        PD_medical_pages = new_list()
    # ---
    return PD_medical_pages


if "__main__" == __name__:
    new_list()
