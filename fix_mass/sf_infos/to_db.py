"""
python3 core8/pwb.py fix_mass/sf_infos/to_db

python3 I:/mdwiki/pybot/fix_mass/sf_infos/to_db.py

python3 pybot/fix_mass/sf_infos/to_db.py

tfj run --mem 2Gi todb --image python3.9 --command "$HOME/local/bin/python3 $HOME/pybot/fix_mass/sf_infos/to_db.py"
tfj run --mem 2Gi todb2 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/sf_infos/to_db"

"""

import re
import sys
import os
import psutil
import json
import tqdm
from pathlib import Path

try:
    from db import insert_all_infos
except Exception as e:
    from fix_mass.sf_infos.db import insert_all_infos

Dir = Path(__file__).parent
all_data_file = Dir / "jsons/sf_infos_all.json"

numbs = 1000 if "2" not in sys.argv else 2


def print_memory():
    yellow, purple = "\033[93m%s\033[00m", "\033[95m%s\033[00m"

    usage = psutil.Process(os.getpid()).memory_info().rss
    usage = usage / 1024 // 1024

    print(yellow % "Memory usage:", purple % f"{usage} MB")


def do_row(url, file):
    # ---
    if not url.startswith("https://prod-images-static.radiopaedia.org/images/"):
        url = f"https://prod-images-static.radiopaedia.org/images{url}"
    # ---
    urlid = ""
    # ---
    # match https://prod-images-static.radiopaedia.org/images/(\d+)/
    ma = re.match(r"https://prod-images-static.radiopaedia.org/images/(\d+)/", url)
    if ma:
        urlid = ma.group(1)
    # ---
    return {
        "url": url,
        "urlid": urlid,
        "file": file,
    }


def start():
    _data_example = {
        "/56189485/IMG-0009-00012.jpg": [
            "File:Epiphyseal aneurysmal bone cyst (Radiopaedia 94033-112655 Coronal 32).jpg",
            "File:Epiphyseal aneurysmal bone cyst (Radiopaedia 94033-112655 Coronal 32).jpg",
            "File:Epiphyseal aneurysmal bone cyst (Radiopaedia 94033-112655 Coronal 3s2).jpg",
        ],
        "/56189481/IMG-0009-00008.jpg": [
            "File:Epiphyseal aneurysmal bone cyst (Radiopaedia 94033-112655 Coronal 33).jpg",
        ],
        "/56189486/IMG-0009-00013.jpg": [
            "File:Epiphyseal aneurysmal bone cyst (Radiopaedia 94033-112655 Coronal 34).jpg",
        ],
    }

    data = {}

    with open(all_data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # split data for list of 100 row
    for i in tqdm.tqdm(range(0, len(data), 100)):
        group = dict(list(data.items())[i : i + 100])
        # ---
        lista = [do_row(k, row[0]) for k, row in group.items() if len(row) == 1]
        # ---
        insert_all_infos(lista, prnt=False)
        # ---
        print_memory()
        # ---
        del group, lista


if __name__ == "__main__":
    start()
