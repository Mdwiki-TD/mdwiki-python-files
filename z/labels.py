"""

python3 core8/pwb.py z/labels

"""

import json
# from newapi.page import NEW_API
from tqdm import tqdm
from pathlib import Path


import api_wd_z

Dir = Path(__file__).parent

# api = NEW_API('en', family='wikipedia')
# api.Login_to_wiki()

qids_file = Dir / "qids.json"
data_file = Dir / "data.json"

to_add = json.loads(data_file.read_text('utf-8')) if data_file.exists() else []

qids_data=json.loads(qids_file.read_text('utf-8')) if qids_file.exists() else {}

qids_data = {z : list(set(v)) for z, v in qids_data.items()}

qids_clean = {x: v[0] for x, v in qids_data.items() if len(v) == 1}

print(f"to_add: {len(to_add)}")

print(f"qids_data: {len(qids_data)}")
print(f"qids_clean: {len(qids_clean)}")

data_to_work = {qid: to_add[en] for en, qid in qids_clean.items() if to_add.get(en)}

print(f"data_to_work: {len(data_to_work)}")

for qid, tab in tqdm(data_to_work.items()):
    # ---
    label = tab["label"]
    desc = tab["desc"]
    # ---
    label_info = api_wd_z.Labels_API(qid, label, "dz")
    desc_info = api_wd_z.Des_API(qid, desc, "dz")
    # ---
    break
