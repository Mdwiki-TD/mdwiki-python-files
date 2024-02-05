'''

python3 core8/pwb.py mass/radio/bots/fix_ids nodump

'''
# ---
import sys
from mass.radio.jsons_files import jsons, dumps_jsons, dump_json_file, urls_to_ids
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, ids=0, all_ids=0, urls_to_get_info=0)
# ---
all_ids = jsons.all_ids.copy()
# ---
print(f"urls_to_ids: {len(urls_to_ids)}")
add = 0
# ---
for caseId, v in jsons.ids.items():
    if caseId in all_ids:
        continue
    all_ids[caseId] = v
    add += 1

# jsons._replace(all_ids = all_ids)
dump_json_file('jsons/all_ids.json', all_ids, False)

print(f"add: {add}")

print("Step 5: Saved jsons.ids dictionary to jsons.")

# Step 5: Save the dictionary to a JSON file
# dumps_jsons(all_ids=1, ids=0)
