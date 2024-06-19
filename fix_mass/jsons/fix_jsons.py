"""

python3 core8/pwb.py fix_mass/jsons/fix_jsons

"""
import tqdm
from pathlib import Path
from fix_mass.fix_sets.jsons_dirs import get_study_dir
from newapi import printe

Dir = Path(__file__).parent

# file = studies_files_infos / f"{study_id}_s_id.json"
# file = "move_text" / f"{study_id}.txt"

dir_to_name = {
    "studies_rev": "rev.json",
    "studies_files_infos": "img_info.json",
    "studies_files": "study_files.json",
    "studies_names": "names.json",
    "move_text": "move.txt",
}

for dir_name, file_name in dir_to_name.items():
    dire = Dir / dir_name
    # ---
    if not dire.exists():
        continue
    # ---
    list_of_files = list(dire.glob("*"))
    # ---
    printe.output("<<red>> ==============")
    # ---
    printe.output(f"fix_jsons: {dir_name}, list_of_files: {len(list_of_files)}")
    # ---
    for file in tqdm.tqdm(list_of_files):
        # ---
        # printe.output(f"{dir_name}/{file.name}")
        # ---
        study_id = str(file.stem).replace("_s_id", "")
        # ---
        # print(study_id)
        # ---
        study_id_dir = get_study_dir(study_id)
        # ---
        new_file = study_id_dir / file_name
        # ---
        new_file.write_text(file.read_text(encoding="utf-8"))
        # ---
        # printe.output(f"<<green>> copy data from [{dir_name}/{file.name}] to \t[{study_id}/{new_file.name}]")
