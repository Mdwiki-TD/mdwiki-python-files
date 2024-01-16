'''

python3 core8/pwb.py mass/radio/fix_ids

'''
import sys
import os
from pathlib import Path
import json

main_dir = Path(__file__).parent
to_work_f = os.path.join(str(main_dir), 'jsons/to_work.json')

ids_file = os.path.join(str(main_dir), 'jsons/ids.json')

with open(ids_file, 'r', encoding='utf-8') as f:
    ids = json.loads(f.read())
new_ids = {}
for url, v in ids.copy().items():
    caseId = v['caseId']
    v['url'] = url
    new_ids[caseId] = v

print("Step 5: Saved the dictionary to 'jsons/ids.json'.")
# Step 5: Save the dictionary to a JSON file
with open(ids_file, 'w', encoding='utf-8') as f:
    json.dump(new_ids, f, ensure_ascii=False, indent=4)
