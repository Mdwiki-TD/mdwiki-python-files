"""

python3 core8/pwb.py z/wikitable ask workibrahem

"""

import json
from pathlib import Path
from newapi.page import MainPage

Dir = Path(__file__).parent


data_file = Dir / "jsons/data.json"
data_tab = json.loads(data_file.read_text('utf-8')) if data_file.exists() else {}
data_tab = {z.lower() : v for z, v in data_tab.items()}
# ---
qids_file = Dir / "jsons/qids.json"
qids_data = json.loads(qids_file.read_text('utf-8')) if qids_file.exists() else {}
qids_data = {z : v for z, v in qids_data.items()}
# ---
one_qid_rows = []
multi_qids_rows = []
zero_qid_rows = []
# ---
for en, e_qids in qids_data.items():
    # ---
    qid_row = ", ".join(f"{{{{Q|{qid}}}}}" for qid in e_qids)
    # ---
    qid_row = qid_row.strip()
    # ---
    label = data_tab.get(en.lower(), {}).get("label", "")
    description = data_tab.get(en.lower(), {}).get("description", "")
    # ---
    n = len(multi_qids_rows) if len(e_qids) > 1 else len(one_qid_rows) if len(e_qids) == 1 else len(zero_qid_rows)
    # ---
    n += 1
    # ---{ "score" : 1, "matched_label" : term, }
    line = f"| {n} \n| {en} \n| {qid_row} \n| {label} \n| {description}"
    # ---
    score = ""
    matched_label = ""
    # ---
    for qid, dd in e_qids.items():
        # ---
        score = dd.get("score", "")
        matched_label = dd.get("matched_label", "")
        # ---
        break
    # ---
    if len(e_qids) > 1:
        multi_qids_rows.append(line)
    elif len(e_qids) == 1:
        line = f"| {n} \n| {en} \n| {qid_row} \n| {score} \n| {matched_label} \n| {label} \n| {description}"
        one_qid_rows.append(line)
    else:
        zero_qid_rows.append(line)
# ---
text_1 = "\n|-\n".join(one_qid_rows)
text_2 = "\n|-\n".join(zero_qid_rows)
text_multi = "\n|-\n".join(multi_qids_rows)
# ---
text = f"""
* All items: {len(qids_data):,}
* [https://editgroups.toolforge.org/b/CB/960017df0e23/ Work Report]

=== with qids ({len(one_qid_rows)}) ===
{{| class="wikitable sortable"
|-
! #
! en
! qid
! score
! matched_label
! label
! description
|-
{text_1}
|-
|}}

=== multi qids ({len(multi_qids_rows)}) ===
{{| class="wikitable sortable"
|-
! #
! en
! qids
! label
! description
|-
{text_multi}
|-
|}}

=== without qids ({len(zero_qid_rows)}) ===
{{| class="wikitable sortable"
|-
! #
! en
! qid
! label
! description
|-
{text_2}
|-
|}}
"""
# ---

title = "User:Mr._Ibrahem/dz2"
# ---
page = MainPage(title, 'www', family='wikidata')

if page.exists():
    oldtext = page.get_text()
    page.save(newtext=text, summary="")
else:
    page.Create(text=text, summary="")
