"""

python3 core8/pwb.py z/data_ready

"""

import json
from pathlib import Path

Dir = Path(__file__).parent

qids_file = Dir / "jsons/qids.json"

results = json.loads(qids_file.read_text('utf-8')) if qids_file.exists() else {}

results_x = {z : list(set(v)) for z, v in results.items()}

data_ready_file = Dir / "jsons/data_ready.json"
data_ready = json.loads(data_ready_file.read_text('utf-8'))

data_ready = {x.lower(): v for x, v in data_ready.items()}
# ---
qid_plus = 0
# ---
for x, qids in results_x.items():
    # ---
    if data_ready.get(x.lower(), {}).get("qid", ""):
        continue
    # ---
    if not qids or len(qids) > 1:
        continue
    # ---
    qid_plus += 1
    # ---
    data_ready[x.lower()]["qid"] = qids[0]
# ---
for x, v in data_ready.copy().items():
    # ---
    if "qid" not in v:
        data_ready[x]["qid"] = ""
# ---
with open(data_ready_file, 'w', encoding='utf-8') as file:
    json.dump(data_ready, file, ensure_ascii=False, indent=4)
# ---
print(f"qid_plus: {qid_plus}")
