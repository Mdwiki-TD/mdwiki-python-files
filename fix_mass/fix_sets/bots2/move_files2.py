"""
s
from fix_mass.fix_sets.bots.move_files2 import to_move_work

"""
import re
# import json
import sys
from pathlib import Path
from newapi import printe
from newapi.ncc_page import NEW_API
from fix_mass.fix_sets.jsons_dirs import get_study_dir#, jsons_dir

api_new = NEW_API("www", family="nccommons")
api_new.Login_to_wiki()

Dir = Path(__file__).parent.parent

move_dir = Dir / "move_text"

if not move_dir.exists():
    move_dir.mkdir()


def change_names(file_dict, ty, study_id):
    modified_file_dict = {}
    new_t = []
    same_title = 0

    for key, value in file_dict.items():
        # key2 like "001", "010", "100"
        key2 = f"0{key}"
        # key2 = f"{key}"
        # ---
        new_key = f"{ty} {key2}"
        # ---
        # new_filename = value.replace(value[value.rfind(" ") + 1 : value.find(").jpg")], new_key)
        ma = re.match(rf"^(.*?-{study_id}) .*? \d+(\)\.\w+)$", value)
        # ---
        if not ma:
            modified_file_dict[value] = value
            same_title += 1
            continue
        # ---
        new_filename = ma.group(1) + " " + new_key + ma.group(2)
        # ---
        if new_filename in new_t:
            printe.output(f"duplicte: {new_filename}")
            return False

        modified_file_dict[value] = new_filename

        new_t.append(new_filename)
    # ---
    # printe.output(f"<<green>> same_title: {same_title}.")
    # ---
    return modified_file_dict


def mv_file(old, new):
    if "mv_test" in sys.argv:
        return True
    move_it = api_new.move(old, new, reason="")
    return move_it


def aa(tab):
    text = ""
    # ---
    for old, new in tab.items():
        na_old = old
        na_new = new
        # ---
        # split old before last -
        try:
            na_old = old.rsplit("-", maxsplit=1)[1].split(" ", maxsplit=1)[1].rsplit(")", maxsplit=1)[0]
            na_new = new.rsplit("-", maxsplit=1)[1].split(" ", maxsplit=1)[1].rsplit(")", maxsplit=1)[0]
        except Exception as e:
            printe.output(f"Error: {e}")
        # ---
        text += f"# [[:{old}|{na_old}]] -> [[:{new}|{na_new}]]\n"
    # ---
    return text


def log(same_titles, diff_titles, study_id):
    # ---
    text = "== same ==\n"

    text += aa(same_titles)
    # ---
    text += "\n== diff ==\n"
    # ---
    text += aa(diff_titles)
    # ---
    study_id_dir = get_study_dir(study_id)
    # ---
    file = study_id_dir / "move.txt"
    # ---
    file2 = move_dir / f"{study_id}.txt"
    # ---
    try:
        with open(file2, "w", encoding="utf-8") as f:
            f.write(text)

    except Exception as e:
        printe.output(f"<<red>> Error writing to file {file}: {str(e)}")
    # ---
    try:
        with open(file, "w", encoding="utf-8") as f:
            f.write(text)

    except Exception as e:
        printe.output(f"<<red>> Error writing to file {file}: {str(e)}")


def mv_files_change_text(text, tab, study_id):
    # ---
    same_titles = {old: new for old, new in tab.items() if old == new}
    # ---
    diff_titles = {old: new for old, new in tab.items() if old != new}
    # ---
    printe.output(f"same_titles: {len(same_titles)}, diff_titles: {len(diff_titles)}")
    # ---
    log(same_titles, diff_titles, study_id)
    # ---
    if "mv" not in sys.argv:
        return text
    # ---
    n_text = text
    # ---
    for old, new in diff_titles.items():
        # ---
        mv = mv_file(old, new)
        # ---
        if mv:
            n_text = n_text.replace(old, new)
    # ---
    return n_text


def to_move_work(text, to_move, study_id):
    # ---
    new_text = text
    # ---
    old_to_new_files = {}
    # ---
    for ty, files in to_move.items():
        # ---
        # if any file start with http return text
        if any(x.startswith("http") for x in files.values()):
            printe.output(f"<<red>> {ty} {len(files)} x.startswith(http)")
            return text
        # ---
        printe.output(f"<<blue>> {ty} {len(files)}")
        # ---
        neww = change_names(files, ty, study_id)
        # ---
        old_to_new_files.update(neww)
    # ---
    if old_to_new_files:
        new_text = mv_files_change_text(new_text, old_to_new_files, study_id)
    # ---
    return new_text
