
"""

Usage:
from mass.radio.st3.PD_medical import PD_medical_pages

New Features:
- Feature 1: Description of feature 1.
- Feature 2: Description of feature 2.

New Commands:
- Command 1: Description of command 1.
- Command 2: Description of command 2.

"""
import json
import os
import re
from pathlib import Path
from newapi.ncc_page import CatDepth
# ---
main_dir = Path(__file__).parent.parent
# ---
pd_file = main_dir / 'jsons/PD_medical_pages.json'
# ---
PD_medical_pages = []
# ---
if not os.path.exists(pd_file):
    with open(pd_file, 'w', encoding='utf-8') as f:
        json.dump(PD_medical_pages, f)
# ---
with open(pd_file, 'r', encoding='utf-8') as f:
    PD_medical_pages = json.load(f)
# ---
def new():
    members = CatDepth("Category:PD medical", sitecode="www", family="nccommons", depth=1, ns="10")
    # ---
    print(f"lenth of members: {len(members)} ")
    with open(pd_file, 'w', encoding='utf-8') as f:
        json.dump(PD_medical_pages, f)

if __name__ == "__main__":
    new()
    # python3 core8/pwb.py mass/radio/st3/PD_medical
    print(f"lenth of PD_medical_pages: {len(PD_medical_pages)} ")