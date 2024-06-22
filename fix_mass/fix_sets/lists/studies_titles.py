"""

python3 core8/pwb.py fix_mass/fix_sets/lists/studies_titles
python3 core8/pwb.py fix_mass/fix_sets/lists/studies_titles nodump

Usage:
from fix_mass.jsons.files import studies_titles, study_to_case_cats


"""
import re
import sys
import json
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


file = jsons_dir / "studies_titles.json"


def read_new(cat, file):
    # ---
    printe.output(f"read_new: {cat=}, {file=}")
    # ---
    file = jsons_dir / file
    # ---
    # read file
    with open(file, "r", encoding="utf-8") as f:
        in_file = json.load(f)
        printe.output(f"<<green>> read {len(in_file)} from {file=}")
    # ---
    sets = get_mem(cat)
    # ---
    new_sets = {k: v for k, v in sets.items() if k not in in_file}
    # ---
    # merge the 2 dictionaries
    new_data = in_file.copy()
    new_data.update(new_sets)
    # ---
    printe.output(f"new_sets: {len(new_sets)}, in_file: {len(in_file)}, new_data: {len(new_data)}")
    # ---
    if "nodump" in sys.argv:
        return
    # ---
    with open(file, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
        printe.output(f"<<green>> write {len(new_data)} to {file=}")


def main():
    cats_files = {
        "Category:Radiopaedia sets": "studies_titles.json",
        "Category:Image set": "studies_titles2.json",
    }
    # ---
    for cat, file in cats_files.items():
        read_new(cat, file)


if __name__ == "__main__":
    main()
