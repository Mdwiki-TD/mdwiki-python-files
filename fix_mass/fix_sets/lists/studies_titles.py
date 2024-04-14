"""

python3 core8/pwb.py fix_mass/fix_sets/lists/studies_titles

Usage:
from fix_mass.fix_sets.jsons.files import studies_titles, study_to_case_cats


"""
import re
import json
import sys
from pathlib import Path
from newapi import printe
from newapi.ncc_page import CatDepth

Dir = Path(__file__).parent.parent

st_dit = Dir / "jsons"
file = st_dit / "studies_titles.json"

members = CatDepth("Category:Radiopaedia sets", sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)

printe.output(f"Radiopaedia sets has: {len(members)} members")

sets = {}
not_match = 0
# ---
for x in members:
    # ---
    ma = re.match(r"^Radiopaedia case .*? id: \d+ study: (\d+)$", x)
    if ma:
        sets[ma.group(1)] = x
    else:
        not_match += 1
# ---
with open(file, "w", encoding="utf-8") as f:
    json.dump(sets, f, ensure_ascii=False, indent=2)
    printe.output(f"<<green>> write {len(sets)} to {file=}")
# ---
printe.output(f"not match: {not_match}")
print(f"{len(sets)=}")