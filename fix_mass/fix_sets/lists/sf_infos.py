"""
python3 core8/pwb.py fix_mass/fix_sets/lists/sf_infos

tfj run --mem 1Gi rdfiles --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/lists/sf_infos read_files"

from fix_mass.fix_sets.lists.sf_infos import from_sf_infos # from_sf_infos(url, study_id)

"""
import sys
import os
import psutil
import json
import tqdm
from newapi import printe
from pathlib import Path

t_dir = Path(__file__).parent.parent / "jsons"
# ---
starts_with = "https://prod-images-static.radiopaedia.org/images"
# ---
sf_infos_file = t_dir / "sf_infos.json"
# ---
if not sf_infos_file.exists():
    sf_infos_file.write_text("{}")
# ---
sfs_infos = {}
# ---
with open(sf_infos_file, "r", encoding="utf-8") as f:
    sfs_infos = json.load(f)


def print_memory():
    _red_ = "\033[91m%s\033[00m"

    usage = psutil.Process(os.getpid()).memory_info().rss
    usage = usage / 1024 // 1024

    print(_red_ % f"memory usage: psutil {usage} MB")


def from_sf_infos(url, study_id):
    # ---
    if url.startswith(starts_with):
        url = url[len(starts_with) :]
    # ---
    lista = sfs_infos.get(url)
    # ---
    if not lista:
        printe.output(f"from_sf_infos: not found: {url}")
        return ""
    # ---
    if len(lista) == 1:
        return lista[0]
    # ---
    printe.output(f"from_sf_infos: {len(lista)}")
    # ---
    for file in lista:
        # File:Persistent trigeminal artery (Radiopaedia 56019-62643 Axial 14).jpg
        staa = f"-{study_id} "
        if staa in file:
            return file
    # ---
    printe.output(f"from_sf_infos: not found: {url}")
    # ---
    return ""


def dumpit():
    printe.output(f"dumpit: {len(sfs_infos)}")
    with open(sf_infos_file, "w", encoding="utf-8") as f:
        json.dump(sfs_infos, f, ensure_ascii=False)
        printe.output(f"<<green>> write {len(sfs_infos)} to file: {sf_infos_file}")


def read_files():
    # ---
    jsons_dir = t_dir / "studies_files_infos"
    list_files = list(jsons_dir.glob("*.json"))
    # ---
    printe.output(f"list_files: {len(list_files)}")
    # ---
    for i in range(0, len(list_files), 1000):
        group = list_files[i : i + 1000]
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
                if img_url not in sfs_infos:
                    sfs_infos[img_url] = []
                # ---
                if file not in sfs_infos[img_url]:
                    sfs_infos[img_url].append(file)
            # ---
            del data
        # ---
        del group
        # ---
        dumpit()
        # ---
        print_memory()
    # ---
    dumpit()


def start():
    # ---
    printe.output(f"sfs_infos: {len(sfs_infos)}")
    # ---
    if "read_files" in sys.argv:
        read_files()
    # ---
    # find urls with more then 1 value
    uls = {k: v for k, v in sfs_infos.items() if len(v) > 1}
    # ---
    # sort it
    uls = {k: v for k, v in sorted(uls.items(), key=lambda item: len(item[1]))}
    # ---
    printe.output(f"uls: {len(uls)}")
    # ---
    for k, v in uls.items():
        printe.output(f"{k}: {len(v)}")


if __name__ == "__main__":
    start()
