"""
python3 core8/pwb.py mass/radio/st3sort/count_files/b

"""
import os
import sys
import tqdm
import json
from pathlib import Path
from mass.radio.bots.studies_utf import studies_urls_to_files_dir
# ---
Dir = Path(__file__).parent
# ---
errors = []
all_files_to_url = {}
count_all_files = 0
# ---
for x in tqdm.tqdm(os.listdir(studies_urls_to_files_dir)):
    # ---
    if not x.endswith(".json"):
        continue
    # ---
    file = studies_urls_to_files_dir / x
    # ---
    try:
        with open(file, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        errors.append(x)
        continue
    # ---
    count_all_files += len(data)
    # ---
    for file, va in data.items():
        all_files_to_url[file] = va["url"]
# ---
print(f"{count_all_files=}")
print(f"{len(all_files_to_url)=}")
# ---
with open(Dir / "all_files_to_url.json", "w", encoding="utf-8") as f:
    json.dump(all_files_to_url, f)
# ---
with open(Dir / "errors.json", "w", encoding="utf-8") as f:
    json.dump(errors, f)
# ---
print(f"{len(errors)=}")
# ---
if "del" in sys.argv:
    for x in errors:
        os.remove(studies_urls_to_files_dir / x)
        print(f"delete {studies_urls_to_files_dir / x}")