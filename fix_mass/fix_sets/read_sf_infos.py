"""
python3 core8/pwb.py fix_mass/fix_sets/read_sf_infos
python3 core8/pwb.py fix_mass/fix_sets/read_sf_infos dump
python3 core8/pwb.py fix_mass/fix_sets/read_sf_infos read_all

tfj run --mem 4Gi readall --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/read_sf_infos read_all"

"""
import sys
import os
import psutil
import json
import tqdm
from newapi import printe
from fix_mass.fix_sets.jsons_dirs import jsons_dir

# ---
numbs = 1000 if "2" not in sys.argv else 2
# ---
starts_with = "https://prod-images-static.radiopaedia.org/images"

sf_infos_dir = jsons_dir / "sf_infos_json"

if not sf_infos_dir.exists():
    sf_infos_dir.mkdir()


def print_memory():
    _red_ = "\033[91m%s\033[00m"

    usage = psutil.Process(os.getpid()).memory_info().rss
    usage = usage / 1024 // 1024

    print(_red_ % f"memory usage: psutil {usage} MB")


def dump_them():
    # ---
    jo_dir = jsons_dir / "studies_files_infos"
    # ---
    list_files = list(jo_dir.glob("*.json"))
    # ---
    printe.output(f"list_files: {len(list_files)}")
    # ---
    for i in range(0, len(list_files), numbs):
        group = list_files[i : i + numbs]
        # ---
        infos_file = sf_infos_dir / f"{i}.json"
        # ---
        if infos_file.exists():
            printe.output(f"exists: {infos_file}")
            continue
        # ---
        infos = {}
        # ---
        for f in tqdm.tqdm(group, total=len(list_files)):
            with open(f, "r", encoding="utf-8") as f:
                data = json.load(f)
            # { "File:Metatarsus adductus (Radiopaedia 62643-70938 Frontal 1).png": { "img_url": "https", "id": 42050951 },}
            for file, v in data.items():
                # print(v)
                img_url = v["img_url"]
                # ---
                if img_url.startswith(starts_with):
                    img_url = img_url[len(starts_with) :]
                # ---
                if img_url not in infos:
                    infos[img_url] = []
                # ---
                if file not in infos[img_url]:
                    infos[img_url].append(file)
            # ---
            del data
        # ---
        printe.output(f"<<green>> write {len(infos)} to file: {infos_file}")
        # ---
        with open(infos_file, "w", encoding="utf-8") as f:
            json.dump(infos, f, ensure_ascii=False)
        # ---
        del group, infos
        # ---
        print_memory()


def read_all():
    all_data = {}
    # ---
    all_data_file = jsons_dir / "sf_infos_all_new.json"
    # ---
    list_files = list(sf_infos_dir.glob("*.json"))
    # ---
    printe.output(f"list_files: {len(list_files)}")
    # ---
    for f in tqdm.tqdm(list_files, total=len(list_files)):
        # ---
        with open(f, "r", encoding="utf-8") as f:
            data = json.load(f)
        # ---
        for img_url, files in data.items():
            # ---
            if img_url not in all_data:
                all_data[img_url] = []
            # ---
            files = [x for x in files if x not in all_data[img_url]]
            # ---
            all_data[img_url].extend(files)
        # ---
        del data
    # ---
    with open(all_data_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False)
    # ---
    printe.output(f"<<green>> write all_data: {len(all_data)} to file: {all_data_file}")
    # ---
    all_data_file_more = jsons_dir / "sf_infos_all_more.json"
    # ---
    urls_with_more = {}
    # ---
    for key, value in all_data.items():
        # ---
        if len(value) > 1:
            urls_with_more[key] = value
    # ---
    with open(all_data_file_more, "w", encoding="utf-8") as f:
        json.dump(urls_with_more, f, ensure_ascii=False)
    # ---
    printe.output(f"<<green>> write urls_with_more: {len(urls_with_more)} to file: {all_data_file_more}")


def start():
    # ---
    all_data_file = jsons_dir / "sf_infos_all_more.json"
    # ---
    urls_with_more = {}
    # ---
    with open(all_data_file, "r", encoding="utf-8") as f:
        urls_with_more = json.load(f)
    # ---
    # sort it
    urls_with_more = {k: v for k, v in sorted(urls_with_more.items(), key=lambda item: len(item[1]))}
    # ---
    printe.output(f"urls_with_more: {len(urls_with_more)}")
    # ---
    for k, v in urls_with_more.items():
        printe.output(f"{k}: {len(v)}")


if __name__ == "__main__":
    if "read_all" in sys.argv:
        read_all()

    elif "dump" in sys.argv:
        dump_them()

    else:
        start()
