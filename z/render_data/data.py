"""
python3 I:/mdwiki/pybot/z/render_data/data.py
"""

import re
import json
from pathlib import Path
import csv

Dir = Path(__file__).parent.parent

data_file = Dir / "jsons/data.json"
csv_file = Dir / "render_data/csv.json"

data = {}
data_Lower = {}

dup = 0

with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        en = row.get("\ufeffEnglish Term") or row.get("English Term")
        # ---
        en = en.strip()
        # ---
        data_Lower.setdefault(en.lower(), 0)
        data_Lower[en.lower()] += 1
        # ---
        label = row["label"].strip()
        description = row["description"].strip()
        # ---
        label = re.sub(r"\s+", " ", label)
        description = re.sub(r"\s+", " ", description)
        # ---
        entry = {
            "label": label,
            "description": description
        }
        # ---
        if en in data and data[en] != entry:
            dup += 1
            continue
        # ---
        data[en] = entry

with open(data_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"dup: {dup}")

data_Lower = {z: v for z, v in data_Lower.items() if v > 1}

print(f"data_Lower: {len(data_Lower)}")
print(data_Lower)
