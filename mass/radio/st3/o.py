"""
python3 core8/pwb.py mass/radio/st3/o 11171
"""
import sys
import json
import os
from pathlib import Path
main_dir = Path(__file__).parent.parent
# ---
from mass.radio.st3.start3 import ids_by_caseId, main
# ---
with open(os.path.join(str(main_dir), 'jsons/all_ids.json'), 'r', encoding='utf-8') as f:
    all_ids = json.load(f)
# ---
# Parsing arguments
lookup_dict = {}
for arg in sys.argv[1:]:
    arg, _, value = arg.partition(':')
    if arg.isdigit():
        print(f"caseId: {arg}")
        case_id = int(arg)
        ta = ids_by_caseId.get(case_id) or ids_by_caseId.get(arg)
        if ta:
            lookup_dict[case_id] = ta
        # ---
        if arg in all_ids:
            print(f'caseId: {arg} in all_ids')
            if "add" in sys.argv:
                lookup_dict[case_id] = all_ids[arg]

# Printing keys and calling main
print(list(lookup_dict.keys()))
main(lookup_dict)
