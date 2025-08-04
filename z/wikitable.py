"""

python3 core8/pwb.py z/wikitable ask workibrahem

"""

import json
from pathlib import Path
from newapi.page import MainPage

Dir = Path(__file__).parent

data_ready_file = Dir / "jsons/data_ready.json"
qids_file = Dir / "jsons/qids.json"

data_ready = json.loads(data_ready_file.read_text('utf-8'))
data_ready = {x.lower(): v for x, v in data_ready.items()}
# ---
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
    label = data_ready.get(en.lower(), {}).get("label", "")
    desc = data_ready.get(en.lower(), {}).get("desc", "")
    # ---
    n = len(multi_qids_rows) if len(e_qids) > 1 else len(one_qid_rows) if len(e_qids) == 1 else len(zero_qid_rows)
    # ---
    n += 1
    # ---
    line = f"| {n} \n| {en} \n| {qid_row} \n| {label} \n| {desc}"
    # ---
    if len(e_qids) > 1:
        multi_qids_rows.append(line)
    elif len(e_qids) == 1:
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

title = "User:Mr._Ibrahem/dz"
# ---
page = MainPage(title, 'www', family='wikidata')

if page.exists():
    oldtext = page.get_text()
    page.save(newtext=text, summary="")
else:
    page.Create(text=text, summary="")
