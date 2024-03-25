"""

python3 core8/pwb.py mass/radio/url_to_sys

"""
import sys
import os
import json
from pathlib import Path
# ---
from mass.radio.jsons_files import jsons, dump_json_file
# jsons.url_to_sys
# dumps_jsons(url_to_sys=0)
# ---
main_dir = Path(__file__).parent
# ---
urls_to_system = {}
# ---
main_dir = Path(__file__).parent
# ---
files_path = main_dir / 'syss/jsons'
# ---
urls_files = [f for f in os.listdir(files_path) if not f.endswith('_infos.json') and f.endswith('.json')]
# ---
for f in urls_files:
    # ---
    system = f.replace('.json', '').replace('_', ' ')
    # ---
    with open(os.path.join(files_path, f), 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    # ---
    print(f'system: {system.ljust(20)} len of urls: {len(data)}')
    # ---
    for url, _ in data.items():
        urls_to_system[url] = system
# ---
dump_json_file('jsons/url_to_sys.json', urls_to_system, False)
# ---
print(f'len of jsons.url_to_sys: {len(jsons.url_to_sys)}')
# ---
# dumps_jsons(url_to_sys=1)
dump_json_file('jsons/url_to_sys.json', jsons.url_to_sys, False)
