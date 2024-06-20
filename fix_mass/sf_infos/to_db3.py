"""
python3 core8/pwb.py fix_mass/sf_infos/to_db3

tfj run --mem 1Gi tdb3 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/sf_infos/to_db3"

"""

import re
import sys
import os
import psutil
import ijson
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

debug = "debug" in sys.argv

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

    # استخدام ijson لقراءة الملف بشكل متدفق
    with open(all_data_file, "r", encoding="utf-8") as f:
        # تعيين مجموعة بيانات فارغة
        data = {}
        # قراءة الكائنات JSON بشكل متدفق
        parser = ijson.parse(f)
        # print(dir(parser))

        current_key = None
        current_value = []

        for prefix, event, value in tqdm.tqdm(parser):
            if debug:
                print("______")
                print(f"prefix: {prefix}")
                print(f"event: {event}")
                print(f"value: {value}")
            # if (prefix, event) == ("item", "start_map"):
            if (prefix, event) == ("", "start_map"):
                current_key = None
                current_value = []

            elif (prefix, event) == ("", "map_key"):
                current_key = value

            elif (prefix, event) == (current_key, "start_array"):
                current_value = []

            elif (prefix, event) == (current_key + ".item", "string"):
                current_value.append(value)

            elif (prefix, event) == (current_key, "end_array"):
                if current_key and current_value:
                    data[current_key] = current_value

                # عند جمع 100 عنصر، قم بمعالجتها
                if len(data) >= numbs:
                    group = dict(list(data.items())[:numbs])
                    lista = [do_row(k, row[0]) for k, row in group.items() if len(row) == 1]
                    insert_all_infos(lista, prnt=False)
                    print_memory()
                    data = {k: data[k] for k in list(data.keys())[numbs:]}

        # معالجة أي عناصر متبقية
        if data:
            lista = [do_row(k, row[0]) for k, row in data.items() if len(row) == 1]
            insert_all_infos(lista, prnt=False)
            print_memory()


if __name__ == "__main__":
    start()
