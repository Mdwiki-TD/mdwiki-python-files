'''

python3 core8/pwb.py mass/radio/bots/add nodump

إضافة البيانات الناقصة من jsons.infos

'''
# ---
import sys
from mass.radio.jsons_files import jsons, dumps_jsons, dump_json_file, urls_to_ids

# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, all_ids=0, urls_to_get_info=0)
# ---
all_ids = jsons.all_ids.copy()
# ---
print(f"urls_to_ids: {len(urls_to_ids)}")
# ---
no_info = 0
added_system = 0
added_author = 0
added_published = 0
# ---
for caseId, v in all_ids.copy().items():
    info = jsons.infos.get(v['url'], {})

    if not info:
        no_info += 1
        continue

    system = v.get('system', '')
    if not system and info.get('system', ''):
        added_system += 1
        all_ids[caseId]['system'] = info.get('system', '')

    author = v.get('author', '')
    if not author and info.get('author', ''):
        added_author += 1
        all_ids[caseId]['author'] = info.get('author', '')

    published = v.get('published', '')
    if not published and info.get('published', ''):
        added_published += 1
        all_ids[caseId]['published'] = info.get('published', '')

dump_json_file('jsons/all_ids.json', all_ids, False)

print("Step 5: Save dictionary to jsons.")

print(f"no_info: {no_info}")
print(f"added_system: {added_system}")
print(f"added_author: {added_author}")
print(f"added_published: {added_published}")
