"""
s
from fix_mass.fix_sets.bots.mv_files import to_move_work

"""
import re
import json
import sys
from pathlib import Path
from newapi import printe

Dir = Path(__file__).parent.parent

st_dit = Dir / "jsons/studies_files"

from newapi.ncc_page import NEW_API

api_new = NEW_API("www", family="nccommons")
api_new.Login_to_wiki()


def dump_it(data):
    for s_id, files in data.items():
        with open(st_dit / f"{s_id}.json", "w", encoding="utf-8") as f:
            json.dump(files, f, ensure_ascii=False, indent=2)
            printe.output(f"<<green>> write {len(files)} to {s_id}.json")


def change_names(file_dict):
    modified_file_dict = {}
    new_t = []

    for key, value in file_dict.items():
        new_key = f"0{key}"

        # new_filename = value.replace(value[value.rfind(" ") + 1 : value.find(").jpg")], new_key)
        ma = re.match(r"^(.*?) \d+(\)\.\w+)$", value)
        if not ma:
            modified_file_dict[value] = value
            continue
        # ---
        new_filename = ma.group(1) + " " + new_key + ma.group(2)
        # ---
        if new_filename in new_t:
            printe.output(f"duplicte: {new_filename}")
            return False

        modified_file_dict[value] = new_filename

        new_t.append(new_filename)

    return modified_file_dict


def mv_file(old, new):
    if "mv_test" in sys.argv:
        return True
    move_it = api_new.move(old, new, reason="")
    return move_it


def mv_files_change_text(text, tab):

    n_text = text
    # ---
    for old, new in tab.items():
        # ---
        mv = mv_file(old, new)
        # ---
        if mv:
            n_text = n_text.replace(old, new)
    # ---
    return n_text


def to_move_work(text, to_move):
    # ---
    new_text = text
    # ---
    if "mv" in sys.argv:
        for ty, files in to_move.items():
            # ---
            # if any file start with http return text
            if any(x.startswith("http") for x in files.values()):
                printe.output(f"<<red>> {ty} {len(files)} x.startswith(http)")
                return text
            # ---
            printe.output(f"<<blue>> {ty} {len(files)}")
            # printe.output(files)
            # ---
            neww = change_names(files)
            # ---
            if neww:
                # ---
                new_text = mv_files_change_text(new_text, neww)
                # printe.output(json.dumps(neww, indent=2))
        # ---
        text = new_text
    # ---
    return text
