"""

python3 core8/pwb.py mass/radio/syss/sys_urls
"""
import sys
import os
import json
from pathlib import Path

# ---
from mass.radio.geturlsnew import get_urls_system, systems, lenth_of_systems
from mass.radio.jsons_files import jsons

# ---
main_dir = Path(__file__).parent
# ---
systems_data = {}
systems_len = {}
# ---
system_to_work = ""
# ---
for arg in sys.argv:
    arg = arg.replace("_", " ")
    if arg in systems:
        system_to_work = arg
# ---
nnno = dict(sorted(lenth_of_systems.items(), key=lambda x: x[1], reverse=True))
# ---
nnno = list(nnno.keys())
# ---
for n, sy in enumerate(nnno, start=10):
    # ---
    sy2 = sy.replace(" ", "_")
    # ---
    if "only" in sys.argv:
        systems_len[sy] = get_urls_system(sy, only_one=True)
    # ---
    ln = lenth_of_systems[sy] * 20
    # ---
    if not system_to_work:
        print(f'tfj run sy{n} --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/syss/sys_urls {sy2}" #{ln:,}')
    # ---
    v = os.path.join(str(main_dir), f"jsons/{sy}.json")
    # ---
    if not os.path.exists(v):
        with open(v, "w", encoding="utf-8") as f:
            f.write("{}")
    # ---
    with open(v, encoding="utf-8") as f:
        systems_data[sy] = json.loads(f.read())
# ---
if "only" in sys.argv:
    for k, v in systems_len.items():
        print(f"{k}: {v}")
# ---
print(f"system_to_work: {system_to_work}")
# ---
if not system_to_work:
    print("<<red>> No system_to_work. Skipping.")
    print("exit()")
    exit()
# ---
if jsons.systems.get(system_to_work):
    print(f"<<green>> system:{system_to_work} already in jsons.systems. Skipping.")
    print("exit()")
    exit()
# ---
len_all = lenth_of_systems.get(system_to_work, 0) * 20
# ---
urls_data = get_urls_system(system_to_work, len_all=len_all)
# ---
if not urls_data:
    print(f"<<red>> No urls_data for system: {system_to_work}")
    print("exit()")
    exit()
# ---
new_urls = {
    x: v['title']
    for x, v in urls_data.items() if x not in systems_data.get(system_to_work, {})
}
# ---
print(f"new_urls: {len(new_urls)}, urls_data: {len(urls_data)}")
# ---
# add new_urls to systems_data[system_to_work]
systems_data[system_to_work].update(new_urls)
# ---
stw_file = os.path.join(str(main_dir), f"jsons/{system_to_work}.json")
# ---
# dump
with open(stw_file, "w", encoding="utf-8") as f:
    json.dump(systems_data[system_to_work], f, ensure_ascii=False, indent=4)
