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

data_ready_file = Dir / "jsons/data_ready.json"

data_ready_list = json.loads(data_ready_file.read_text('utf-8')) if data_ready_file.exists() else {}

print(f"data_ready_list: {len(data_ready_list)}")

data_to_work = {v["qid"]: data_ready_list[k] for k, v in data_ready_list.items() if v["qid"]}

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
    same_label += labels_dz == label
    same_desc += descriptions_dz == desc
    # ---
    diff_label += (labels_dz != label) if not labels_dz else 0
    diff_desc += (descriptions_dz != desc) if not descriptions_dz else 0
    # ---
    if not labels_dz:
        label_info = api_wd_z.Labels_API(qid, label, "dz")
    # ---
    if not descriptions_dz:
        desc_info = api_wd_z.Des_API(qid, desc, "dz")
    # ---
    if "break" in sys.argv and (not descriptions_dz or not labels_dz):
        print("break")
        break

print(f"same_label: {same_label}")
print(f"same_desc: {same_desc}")
