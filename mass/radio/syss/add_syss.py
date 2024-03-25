"""

python3 core8/pwb.py mass/radio/syss/add_syss nodump


"""

import json
import os
# ---
from pathlib import Path

from newapi import printe

from mass.radio.geturlsnew import lenth_of_systems
from mass.radio.jsons_files import dump_json_file, jsons

# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, all_ids=0, urls_to_get_info=0)
# ---
main_dir = Path(__file__).parent
# ---
files_path = main_dir / "jsons"
# ---
# read all jsons files in main_dir and append urls to sys_urls
# ---
infos_files = [f for f in os.listdir(files_path) if f.endswith("_infos.json")]
urls_files = [
    f for f in os.listdir(files_path)
    if not f.endswith("_infos.json") and f.endswith(".json")
]
# ---
sys_urls = {}
# ---
printe.output(f"<<green>> urls_files: {len(urls_files)}")


# ---
def po(file, data, lnn):
    if len(data) < lnn and (lnn - len(data)) > 10:
        da = f"{len(data):,},".ljust(10)
        la = f"{lnn:,},".ljust(10)
        print(f"len: {da} lnn: {la} file: {file}")


# ---
for file in urls_files:
    # ---
    with open(os.path.join(files_path, file), encoding="utf-8") as f:
        data = json.loads(f.read())
    # ---
    lnn = (lenth_of_systems[file.replace(".json", "")] * 20) - 10
    # ---
    po(file, data, lnn)
    # ---
    sys_urls.update(data)
# ---
print(f"len of sys_urls: {len(sys_urls)}")
# ---
new_urls = {k: v for k, v in sys_urls.items() if k not in jsons.urls}
# ---
print(f"len of new_urls: {len(new_urls)}, jsons.urls: {len(jsons.urls)}")
# ---
jsons.urls.update(new_urls)
# ---
dump_json_file("jsons/urls.json", jsons.urls, False)
# ---

# ---
printe.output(f"<<green>> infos_files: {len(infos_files)}")
get_infos = {}
# ---
for file in infos_files:
    # ---
    with open(os.path.join(files_path, file), encoding="utf-8") as f:
        data = json.loads(f.read())
    # ---
    lnn = (lenth_of_systems[file.replace("_infos.json", "")] * 20) - 10
    # ---
    # po(file, data, lnn)
    # ---
    get_infos.update(data)
# ---
new_infos = {k: v for k, v in get_infos.items() if k not in jsons.infos}
# ---
print(f"len of get_infos: {len(get_infos)}")
# ---
print(f"len of new_infos: {len(new_infos)}, jsons.infos: {len(jsons.infos)}")
# ---
jsons.infos.update(new_infos)
# ---
dump_json_file("jsons/infos.json", jsons.infos, False)
