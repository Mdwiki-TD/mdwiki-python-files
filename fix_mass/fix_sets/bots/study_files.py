"""

from fix_mass.fix_sets.bots.study_files import get_study_files

"""
import re
import json
import sys
from pathlib import Path
from newapi import printe
from newapi.ncc_page import CatDepth

Dir = Path(__file__).parent.parent

st_dit = Dir / "jsons/studies_files"

from fix_mass.fix_sets.jsons.files import studies_titles, study_to_case_cats


def dump_it(data):
    for s_id, files in data.items():
        with open(st_dit / f"{s_id}.json", "w", encoding="utf-8") as f:
            json.dump(files, f, ensure_ascii=False, indent=2)
            printe.output(f"<<green>> write {len(files)} to {s_id}.json")


def filter_members(cat_members):
    data = {}
    # ---
    not_match = 0
    # ---
    for x in cat_members:
        # ---
        if not x.startswith("File:"):
            printe.output(f"!{x}")
            continue
        # ---
        # search for (Radiopaedia \d+-\d+
        se = re.match(r".*?\(Radiopaedia \d+-(\d+)", x)
        # ---
        if not se:
            printe.output(f"!{x}")
            not_match += 1
            continue
        # ---
        study_id = se.group(1)
        # ---
        if study_id not in data:
            data[study_id] = []
        # ---
        data[study_id].append(x)
    # ---
    printe.output(f"len {not_match=}")
    # ---
    dump_it(data)
    # ---
    return data


def get_study_files(study_id):
    # ---
    file = st_dit / f"{study_id}.json"
    # ---
    if file.exists():
        printe.output(f"<<green>> get_study_files: {study_id}.json exists")
        with open(file, encoding="utf-8") as f:
            return json.load(f)
    # ---
    cat = study_to_case_cats.get(study_id)
    # ---
    if not cat:
        printe.output(f"!{study_id} not found")
        return
    # ---
    cat_members = CatDepth(cat, sitecode="www", family="nccommons", depth=0)
    # ---
    filterd = filter_members(cat_members)
    # ---
    result = filterd.get(study_id)
    # ---
    if not result:
        printe.output(f"!{study_id} not found")
        return
    # ---
    return result
