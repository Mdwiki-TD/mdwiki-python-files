# -*- coding: utf-8 -*-
"""
python3 core8/pwb.py mass/eyerounds/added

"""
import sys
import json
from pathlib import Path

main_dir = Path(__file__).parent
jsonimages = main_dir / 'jsons/images.json'


with open(jsonimages, "r") as file:
    data = json.load(file)

# read file cases_list.txt
with open(main_dir / "cases_list.txt", "r", encoding="utf-8") as f:
    lines = [x.strip() for x in f.readlines() if x.strip() and x.strip() not in data]

for line in lines:
    data[line] = {"authors": {}, "date": "", "images": {}}
print(f"Added {len(lines)} new urls to json")

# sort data by key
data = dict(sorted(data.items(), key=lambda item: item[0]))

# Save the updated json_data back to the JSON file
with open(jsonimages, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)
