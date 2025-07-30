"""

python3 core8/pwb.py z/labels

python3 core8/pwb.py z/labels ask workhimo break


"""

import json
import sys
# from newapi.page import NEW_API
from tqdm import tqdm
from pathlib import Path

import api_wd_z
from apis.wd_bots import wd_rest_new

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

same_label = 0
same_desc = 0

diff_label = 0
diff_desc = 0

for qid, tab in tqdm(data_to_work.items()):
    # ---
    label = tab["label"]
    desc = tab["desc"]
    # ---
    item_data = wd_rest_new.Get_one_qid_info(qid)
    # ---
    labels = item_data.get("labels", {})
    descriptions = item_data.get("descriptions", {})
    # ---
    labels_dz = labels.get("dz", "")
    descriptions_dz = descriptions.get("dz", "")
    # ---
    if not labels_dz:
        label_info = api_wd_z.Labels_API(qid, label, "dz")
    elif labels_dz == label:
        same_label += 1
    else:
        diff_label += 1
        print(f"labels_dz: {labels_dz}")
    # ---
    if not descriptions_dz:
        desc_info = api_wd_z.Des_API(qid, desc, "dz")
    elif descriptions_dz == desc:
        same_desc += 1
    else:
        diff_desc += 1
        print(f"descriptions_dz: {descriptions_dz}")
    # ---
    if "break" in sys.argv:
        break

print(f"same_label: {same_label}")
print(f"same_desc: {same_desc}")
