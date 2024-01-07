'''

python3 core8/pwb.py mass/radio/to_work

'''
import os
from pathlib import Path
import json

main_dir = Path(__file__).parent
urlsfile = os.path.join(str(main_dir), 'jsons/urls.json')

if not os.path.exists(urlsfile):
    with open(urlsfile, 'w', encoding='utf-8') as f:
        f.write("{}")

with open(urlsfile, 'r', encoding='utf-8') as f:
    all_urls = json.loads(f.read())
print(f"lenth of all_urls: {len(all_urls)}")

cases_file = os.path.join(str(main_dir), 'jsons/cases.json')

with open(cases_file, 'r', encoding='utf-8') as f:
    cases_in = json.loads(f.read())

print(f"lenth of cases_in: {len(cases_in)}")

# items in all_urls and not in cases_in
to_work = {item :va for item, va in all_urls.items() if va not in cases_in.values()}

print(f"lenth of to_work: {len(to_work)}")

# dump to_work to to_work.json
with open(os.path.join(str(main_dir), 'jsons/to_work.json'), 'w', encoding='utf-8') as f:
    json.dump(to_work, f, ensure_ascii=False, indent=4)