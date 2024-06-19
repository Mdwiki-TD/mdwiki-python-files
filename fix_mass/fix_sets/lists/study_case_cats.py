"""

python3 core8/pwb.py fix_mass/fix_sets/lists/study_case_cats

Usage:
from fix_mass.fix_sets.jsons.files import studies_titles, study_to_case_cats

# ---

"""
import tqdm
import json
from pathlib import Path

from mass.radio.jsons_files import jsons

#  jsons.all_ids
#  jsons.cases_cats
main_dir = Path(__file__).parent.parent
# ---
all_ids = jsons.all_ids.copy()
# ---
cases_cats_list = jsons.cases_cats.copy()
# ---
study_to_case_cats = {}
# ---
no_cats = []
# ---
for _, va in tqdm.tqdm(all_ids.items()):
    # ---
    caseId = va["caseId"]
    # ---
    if not caseId:
        print(f"\nno caseId: {caseId}")
        print(va)
        continue
    # ---
    case_cat = cases_cats_list.get(caseId) or cases_cats_list.get(str(caseId))
    # ---
    if not case_cat:
        no_cats.append(caseId)
        print(f"add {caseId=} to no cats")
        continue
    # ---
    studies = [study.split("/")[-1] for study in va["studies"]]
    # ---
    # print(studies)
    # ---
    for study in studies:
        study_to_case_cats[study] = case_cat
# ---
print(f"no cats: {len(no_cats)}")
print(f"{len(study_to_case_cats)=}")
# ---
if __name__ == "__main__":
    file = main_dir / "jsons/study_to_case_cats.json"

    with open(file, "w", encoding="utf-8") as f:
        json.dump(study_to_case_cats, f, ensure_ascii=False, indent=2)
