"""

python3 core8/pwb.py mass/radio/bots/fix_ids nodump

إضافة العناوين الناقصة من
jsons.ids
إلى
jsons.all_ids

"""

# ---

from mass.radio.jsons_files import dump_json_file, jsons, urls_to_ids

# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, all_ids=0, urls_to_get_info=0)
# ---
all_ids = jsons.all_ids.copy()
# ---
print(f"urls_to_ids: {len(urls_to_ids)}")
add = 0
add_va = 0
# ---
for caseId, v in jsons.ids.items():
    if caseId in all_ids:
        v_in = all_ids[caseId]
        # ---
        for k, v2 in v.items():
            v1 = v_in.get(k, "")
            if v2 and not v1:
                add_va += 1
                all_ids[caseId][k] = v2
                print(f"add_va: {k} = {v2}")

    else:
        all_ids[caseId] = v
        add += 1
# ---
params = {
    "caseId": 0,
    "title": "",
    "studies": [],
    "url": "",
    "system": "",
    "author": "",
    "published": "",
}
# ---
added_key = 0
# ---
for caseId, v in all_ids.copy().items():
    if caseId not in jsons.ids:
        jsons.ids[caseId] = v
    for k, v2 in params.items():
        if k not in v:
            all_ids[caseId][k] = v2
            added_key += 1
# ---
added_key_to_ids = 0
# ---
for caseId, v in jsons.ids.copy().items():
    for k, v2 in params.items():
        v2 = all_ids.get(caseId, {}).get(k, v2)
        if not v.get(k):
            jsons.ids[caseId][k] = v2
            added_key_to_ids += 1
# ---
# jsons._replace(all_ids = all_ids)
dump_json_file("jsons/all_ids.json", all_ids, False)
dump_json_file("jsons/ids.json", jsons.ids, False)
# ---
print(f"add: {add}")
print(f"add_va: {add_va}")
print(f"added_key: {added_key}")
print(f"added_key_to_ids: {added_key_to_ids}")
# ---
print("Step 5: Saved jsons.ids dictionary to jsons.")

# Step 5: Save the dictionary to a JSON file
# dumps_jsons(all_ids=1, ids=0)
