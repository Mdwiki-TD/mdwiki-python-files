"""

python3 core8/pwb.py z/labels

python3 core8/pwb.py z/labels ask workhimo break


"""

import json
import sys
# from newapi.page import NEW_API
from tqdm import tqdm
from pathlib import Path

from api_z import api_wd_z
from apis.wd_bots import wd_rest_new

Dir = Path(__file__).parent

# api = NEW_API('en', family='wikipedia')
# api.Login_to_wiki()

data_to_work_file = Dir / "jsons/data_to_upload.json"


def get_best_qid(e_qids):
    # ---
    qid_main = ""
    best_label = None
    highest_score = 0.0
    # ---
    for qid, dd in e_qids.items():
        # ---
        score = dd.get("score", "")
        label = dd.get("matched_label", "")
        # ---
        if score > highest_score:
            highest_score = score
            best_label = label
            qid_main = qid
    # ---
    return qid_main, highest_score, best_label


def make_data_to_work():
    # ---
    # data_to_work = "epiglottic": { "label": "ལྕེ་ཅུངམ།", "desc": "ལྕེ་ཅུངམ་འདི་གིས་ ཆུ་དང་བཞེས་སྒོའི་རིགས་ཚུ་ ལམ་འཛྫོལ་", "qid": "Q18557843", "score": 0.741, "matched_label": "epiglottis cancer" }
    # ---
    data_file = Dir / "jsons/data.json"
    data_tab = json.loads(data_file.read_text('utf-8')) if data_file.exists() else {}
    data_tab = {z.lower() : v for z, v in data_tab.items()}
    # ---
    qids_file = Dir / "jsons/qids.json"
    results_x = json.loads(qids_file.read_text('utf-8')) if qids_file.exists() else {}
    # "epiglottic": { "Q18557843": { "score": 0.741, "matched_label": "epiglottis cancer" } }
    results = {z : v for z, v in results_x.items()}
    # ---
    print(f"results : {len(results)}")
    # ---
    data_to_work = {}
    # ---
    for en, e_qids in results.items():
        # ---
        label = data_tab.get(en.lower(), {}).get("label", "")
        desc = data_tab.get(en.lower(), {}).get("desc", "")
        # ---
        qid, score, matched_label = get_best_qid(e_qids)
        # ---
        data_to_work[en] = {
            "label": label,
            "desc": desc,
            "qid": qid,
            "score": score,
            "matched_label": matched_label,
        }
    # ---
    print(f"data_to_work: {len(data_to_work)}")
    # ---
    data_to_work = dict(sorted(data_to_work.items()))
    # ---
    with open(data_to_work_file, 'w', encoding='utf-8') as file:
        json.dump(data_to_work, file, ensure_ascii=False, indent=4)
    # ---
    return data_to_work


def work_in_list(data_to_work):

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


def main():
    data_to_work = make_data_to_work()
    # ---
    work_in_list(data_to_work)


def test():
    # python3 core8/pwb.py z/labels test
    # ---
    tab = {
        "Q111665793": {
            "score": 0,
            "matched_label": ""
        },
        "Q2026556": {
            "score": 1,
            "matched_label": "operating table"
        },
        "xsxs": {
            "score": 1.001,
            "matched_label": "zzz table"
        }
    }
    # ---
    qid, score, matched_label = get_best_qid(tab)
    # ---
    print(f"result: qid: {qid} \t score: {score} \t matched_label: {matched_label}")


if __name__ == '__main__':
    if "test" in sys.argv:
        test()
    else:
        main()
