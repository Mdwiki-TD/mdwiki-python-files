'''

python3 core8/pwb.py mass/radio/bots/add

'''
# ---
import sys
from mass.radio.jsons_files import jsons, dumps_jsons, dump_json_file, urls_to_ids
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, ids=0, all_ids=0, urls_to_get_info=0)
# ---
all_ids = jsons.all_ids.copy()
# ---
print(f"urls_to_ids: {len(urls_to_ids)}")
# ---
for caseId, v in all_ids.copy().items():
    url = v['url']
    info = {}
    if url in jsons.infos:
        info = jsons.infos[url]
    all_ids[caseId]['system'] = info.get('system', '')
    all_ids[caseId]['author'] = info.get('author', '')
    all_ids[caseId]['published'] = info.get('published', '')
        
dump_json_file('jsons/all_ids.json', all_ids, False)

print("Step 5: Saved jsons.ids dictionary to jsons.")
