"""

python3 core8/pwb.py fix_mass/fix_sets/lists/studies_titles
python3 core8/pwb.py fix_mass/fix_sets/lists/studies_titles nodump
python3 core8/pwb.py fix_mass/fix_sets/lists/studies_titles nodump fix_2

Usage:
from fix_mass.jsons.files import studies_titles, study_to_case_cats


"""
import re
import sys
import json
from newapi import printe
from newapi.ncc_page import CatDepth

from fix_mass.fix_sets.jsons_dirs import jsons_dir

mem_cach = {}


def get_mem(title):
    members = CatDepth(title, sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)
    # ---
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
    mem_cach[title] = sets
    # ---
    return sets


def dumpit(file, data):
    file = jsons_dir / file
    # ---
    if "nodump" in sys.argv:
        return
    # ---
    # sort data
    data = dict(sorted(data.items(), key=lambda x: x[0]))
    # ---
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        printe.output(f"<<green>> write {len(data)} to {file=}")


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
    return new_data


def fix_2():
    # ---
    file1 = jsons_dir / "studies_titles.json"
    file2 = jsons_dir / "studies_titles2.json"
    # ---
    with open(file1, "r", encoding="utf-8") as f:
        data_1 = json.load(f)
        printe.output(f"<<green>> read {len(data_1)} from {file1=}")
    # ---
    with open(file2, "r", encoding="utf-8") as f:
        data_2 = json.load(f)
        printe.output(f"<<green>> read {len(data_2)} from {file2=}")
    # ---
    # items in data_2 and not in data_1
    new_data = {x: v for x, v in data_2.items() if x not in data_1}
    # ---
    printe.output(f"len(new_data): {len(new_data)}")
    # ---
    dumpit("studies_titles2.json", new_data)


def main():
    cats_files = {
        "Category:Radiopaedia sets": "studies_titles.json",
        "Category:Image set": "studies_titles2.json",
    }
    # ---
    data_all = {}
    # ---
    for cat, file in cats_files.items():
        # ---
        data = read_new(cat, file)
        # ---
        data_all[file] = data
        # ---
        dumpit(file, data)
    # ---
    fix_2()


if __name__ == "__main__":
    if "fix_2" in sys.argv:
        fix_2()
    else:
        main()
