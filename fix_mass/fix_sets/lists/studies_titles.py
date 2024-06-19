"""

python3 core8/pwb.py fix_mass/fix_sets/lists/studies_titles

Usage:
from fix_mass.jsons.files import studies_titles, study_to_case_cats


"""
import re
import json
import sys
from pathlib import Path
from newapi import printe
from newapi.ncc_page import CatDepth

from fix_mass.fix_sets.jsons_dirs import jsons_dir


def get_mem(title):
    members = CatDepth(title, sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)

    sets = {}
    not_match = 0
    # ---
    for x in members:
        # ---
        ma = re.match(r"^Radiopaedia case .*? id: \d+ study: (\d+)$", x)
        ma2 = re.match(r"^.*? \(Radiopaedia \d+-(\d+) .*?$", x)
        # ---
        if ma:
            sets[ma.group(1)] = x
        elif ma2:
            sets[ma2.group(1)] = x
        else:
            not_match += 1
    # ---
    printe.output(f"title: {title}")
    printe.output(f"\tmembers: {len(members)}")
    printe.output(f"\tnot match: {not_match}")
    printe.output(f"\t{len(sets)=}")
    # ---
    return sets


# ---
sets = get_mem("Category:Radiopaedia sets")
# ---
file = jsons_dir / "studies_titles.json"
# ---
with open(file, "w", encoding="utf-8") as f:
    json.dump(sets, f, ensure_ascii=False, indent=2)
    printe.output(f"<<green>> write {len(sets)} to {file=}")
# ---
sets2 = get_mem("Category:Image set")
# ---
file2 = jsons_dir / "studies_titles2.json"
# ---
with open(file2, "w", encoding="utf-8") as f:
    json.dump(sets2, f, ensure_ascii=False, indent=2)
    printe.output(f"<<green>> write {len(sets2)} to {file2=}")
# ---
