"""

python3 core8/pwb.py mass/radio/st3/miss

tfj run miss --image python3.9 --command "$HOME/local/bin/python3 c8/pwb.py mass/radio/st3/miss"

"""
import sys
import json
import os
from pathlib import Path
from mass.radio.st3sort.start3 import main

# ---
main_dir = Path(__file__).parent.parent
with open(os.path.join(str(main_dir), "jsons/all_ids.json"), encoding="utf-8") as f:
    all_ids = json.load(f)
# ---
lista = """
    182746
    """
# ---
new_ids = [x.strip() for x in lista.split("\n") if x.strip()]
# ---
# Parsing arguments
lookup_dict = {x: (all_ids.get(x) or all_ids.get(int(x))) for x in new_ids if x in all_ids}

print(f"len new_ids: {len(new_ids)}")
print(f"len lookup_dict: {len(lookup_dict)}")
# ---
if "start" in sys.argv:
    main(lookup_dict)
