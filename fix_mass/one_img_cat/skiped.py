"""

tfj run cdcf --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/one_img_cat/skiped"

python3 core8/pwb.py fix_mass/one_img_cat/skiped from_files ask
python3 core8/pwb.py fix_mass/one_img_cat/skiped files ask
python3 core8/pwb.py fix_mass/one_img_cat/skiped ask

العمل على المقالات التي بها صورة واحدة فقط

"""
import json
import tqdm
import re
import sys
from pathlib import Path
from newapi import printe
from newapi.ncc_page import MainPage as ncc_MainPage

from fix_mass.fix_sets.bots2.text_cat_bot import add_cat_to_set#, fix_cats
from fix_mass.fix_sets.bots2.filter_ids import filter_no_title
from fix_mass.fix_sets.bots2.done2 import filter_done
from fix_mass.fix_sets.bots.stacks import get_stacks  # get_stacks(study_id)
from fix_mass.fix_sets.jsons_dirs import st_ref_infos
from fix_mass.jsons.files import studies_titles

Dir = Path(__file__).parent
count_cach = {}


def update_text(title, study_id):
    # ---
    printe.output(f"<<yellow>> update_text: {title}")
    # ---
    page = ncc_MainPage(title, "www", family="nccommons")
    # ---
    p_text = page.get_text()
    new_text = p_text
    # ---
    if new_text.find("Category:Sort studies fixed") == -1:
        new_text += "\n[[Category:Sort studies fixed]]"
    # ---
    if new_text.find("[[Category:Radiopaedia case ") == -1:
        new_text = add_cat_to_set(new_text, study_id, title)
    # ---
    if new_text.strip() == p_text.strip():
        printe.output("no changes..")
        return
    # ---
    page.save(newtext=new_text, summary="Added [[:Category:Sort studies fixed]]")


def count_files(study_id):
    # ---
    if count_cach.get(study_id):
        return count_cach[study_id]
    # ---
    stacks_data = get_stacks(study_id)
    # ---
    all_files = []
    # ---
    for x in stacks_data:
        all_files.extend([x["public_filename"] for x in x["images"]])
    # ---
    all_files = list(set(all_files))
    # ---
    count_cach[study_id] = len(all_files)
    # ---
    return len(all_files)


def one_st(study_id, study_title):
    # ---
    printe.output(f"_____________\n {study_id=}, {study_title=}")
    # ---
    all_files = count_files(study_id)
    # ---
    printe.output(f"all_files: {all_files}")
    # ---
    if all_files > 1:
        return False
    # ---
    update_text(study_title, study_id)


def from_files():
    lisst_of_s = []
    # ---
    files_file = Dir / "studies_one_file.json"
    # ---
    if not files_file.exists():
        files_file.write_text("[]")
    # ---
    if "from_files" in sys.argv:
        with open(files_file, "r", encoding="utf-8") as f:
            lisst_of_s = json.load(f)
        if lisst_of_s:
            return lisst_of_s
    # ---
    for subdir in tqdm.tqdm(st_ref_infos.iterdir(), total=80000):
        # ---
        if not subdir.is_dir():
            continue
        # ---
        study_id = subdir.name
        # ---
        file_js = subdir / "stacks.json"
        # ---
        if not file_js.exists():
            continue
        # ---
        lisst_of_s.append(study_id)
    # ---
    with open(files_file, "w", encoding="utf-8") as f:
        json.dump(lisst_of_s, f, ensure_ascii=False, indent=2)
    # ---
    return lisst_of_s


def main(ids):
    # ---
    if not ids:
        # ---
        if "files" in sys.argv or "from_files" in sys.argv:
            ids = from_files()
            printe.output(f"<<yellow>> ids from_files: {len(ids):,}")
        else:
            ids = list(studies_titles.keys())
            printe.output(f"<<yellow>> ids from studies_titles: {len(ids):,}")
    # ---
    ids_titles = filter_no_title(ids)
    # ---
    ids_titles = filter_done(ids_titles)
    # ---
    ids_titles = {k: v for k, v in ids_titles.items() if count_files(k) == 1}
    # ---
    printe.output(f"<<yellow>> titles_only_one: {len(ids_titles):,}")
    printe.output(f"<<yellow>> titles_only_one: {len(ids_titles):,}")
    printe.output(f"<<yellow>> titles_only_one: {len(ids_titles):,}")
    # ---
    for study_id, study_title in ids_titles.items():
        one_st(study_id, study_title)


if __name__ == "__main__":
    ids = [arg.strip() for arg in sys.argv if arg.strip().isdigit()]
    # ---
    main(ids)
