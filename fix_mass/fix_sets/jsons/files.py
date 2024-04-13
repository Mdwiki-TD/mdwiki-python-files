"""
from fix_mass.fix_sets.jsons.files import studies_titles, study_to_case_cats
"""
import json
from pathlib import Path
from newapi import printe

jsons_dir = Path(__file__).parent
# ---
studies_titles = {}
study_to_case_cats = {}
# ---
with open( jsons_dir / "studies_titles.json", "r", encoding="utf-8") as f:
    studies_titles = json.load(f)
    print(f"{len(studies_titles)=}")
# ---
with open( jsons_dir / "study_to_case_cats.json", "r", encoding="utf-8") as f:
    study_to_case_cats = json.load(f)
    print(f"{len(study_to_case_cats)=}")
