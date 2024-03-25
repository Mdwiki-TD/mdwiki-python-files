"""

python3 core8/pwb.py mass/radio/syss/sys_infos
python3 core8/pwb.py mass/radio/syss/sys_infos todo

"""

import json
import os
import sys
from pathlib import Path

# ---
from mass.radio.geturlsnew import get_urls_system, lenth_of_systems, systems
from mass.radio.jsons_files import jsons

# ---
ma_infos = list(jsons.infos.copy().keys())
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
def get_to_do(k):
    stw_file = os.path.join(str(main_dir), f"jsons/{k}.json")
    # ---
    # dump
    with open(stw_file, encoding="utf-8") as f:
        urls_sys = json.loads(f.read())
    # ---
    to_do = [url for url in urls_sys.keys() if url not in ma_infos]
    # ---
    return to_do


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
    if "todo" in sys.argv:
        to_do = get_to_do(sy)
        if to_do:
            print(f"system: {sy.ljust(25)} to_do: {str(len(to_do)).ljust(15)} len_system_urls: {ln:,}")
        continue
    # ---
    if not system_to_work:
        print(f'tfj run syi{n} --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/syss/sys_infos {sy2}" #{ln:,}')
    # ---
    v = os.path.join(str(main_dir), f"jsons/{sy}_infos.json")
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
if not system_to_work:
    print("<<red>> No system_to_work. Skipping.")
    print("exit()")
    exit()
# ---
to_do = get_to_do(system_to_work)
# ---
print(f"system_to_work: {system_to_work}, to_do: {len(to_do)}")
# ---
print(f"system_to_work: {system_to_work}")
# ---
if not to_do:
    print(f"<<red>> No to_do for system: {system_to_work}")
    print("exit()")
    exit()
# ---
len_all = lenth_of_systems.get(system_to_work, 0) * 20
# ---
u_data = get_urls_system(system_to_work, return_tab=True, len_all=len_all)
# ---
if not u_data:
    print(f"<<red>> No u_data for system: {system_to_work}")
    print("exit()")
    exit()
# ---
new_infos = {x: v for x, v in u_data.items() if x not in ma_infos}
# ---
print(f"new_infos: {len(new_infos)}")

stw_infos_file = os.path.join(str(main_dir), f"jsons/{system_to_work}_infos.json")

# dump infos
with open(stw_infos_file, "w", encoding="utf-8") as f:
    json.dump(new_infos, f, ensure_ascii=False, indent=4)
