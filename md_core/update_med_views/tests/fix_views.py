#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/tests/fix_views

"""
import tqdm
import sys
import json
from pathlib import Path

t_dump_dir = Path(__file__).parent.parent / "views"

to_fix = 1

for year_dir in t_dump_dir.glob("*"):
    # ---
    files = [x for x in year_dir.glob("*.json")]
    # ---
    for n, json_file in enumerate(files, start=1):
        # ---
        name = json_file.name
        # ---
        print(f"== f {n}/{len(files)}: {name}")
        # ---
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        # ---
        # "Dlóóʼ binaalniih": { "all": 895, "2023": { "all": 895, "202301": 64, "202302": 64, "202303": 75, "202304": 80, "202305": 65, "202306": 93, "202307": 96, "202308": 79, "202309": 70, "202310": 78, "202311": 69, "202312": 62 } }
        # ---
        new_data = {}
        # ---
        for title, v in data.items():
            # ---
            title = title.replace("_", " ")
            # ---
            new_data[title] = {}
            # ---
            for key, value in v.items():
                if isinstance(value, int):
                    new_data[title][key] = value
                elif isinstance(value, dict):
                    new_data[title][key] = value.get("all", value)
        # ---
        if data == new_data:
            continue
        # ---
        print(f"file: {name} changed..")
        # ---
        to_fix += 1
        # ---
        if "fix" in sys.argv:
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(new_data, f, ensure_ascii=False, indent=2)

print(f"files to fix: {to_fix}")
