"""
python3 core8/pwb.py z/data
"""

import re
import json
from pathlib import Path
import csv

Dir = Path(__file__).parent

data_file = Dir / "jsons/data.json"
csv_file = Dir / "dictionary(ocr_resolved).csv"

data = {}

dup = 0

with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        en = row.get("\ufeffEnglish Term") or row.get("English Term")
        # ---
        en = en.strip()
        # ---
        label = row["Dzongkha Term"].strip()
        desc = row["Dzongkha Explanation"].strip()
        # ---
        label = re.sub(r"\s+", " ", label)
        desc = re.sub(r"\s+", " ", desc)
        # ---
        entry = {
            "label": label,
            "desc": desc
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
