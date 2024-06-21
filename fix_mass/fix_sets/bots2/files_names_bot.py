"""

from fix_mass.fix_sets.bots2.files_names_bot import get_files_names, get_cach

"""
import re
import json
import tqdm
import sys

# from pathlib import Path
from newapi import printe
from fix_mass.fix_sets.bots2.find_from_url import find_file_name_from_url
from fix_mass.fix_sets.lists.sf_infos import from_sf_infos  # from_sf_infos(url, study_id)
from fix_mass.fix_sets.bots2.get_rev import get_images_ids, get_file_urls_new  # get_file_urls_new(study_id)
from fix_mass.fix_sets.jsons_dirs import get_study_dir
from fix_mass.dp_infos.db_duplict import insert_all_infos
from fix_mass.file_infos.db import find_data  # find_data(url="", urlid="", file="")

data_uu = {}

# studies_names_dir = jsons_dir / "studies_names"


def dump_it(data2, cach, study_id):
    # ---
    # file = studies_names_dir / f"{study_id}.json"
    # ---
    data = cach.copy()
    # ---
    for x in data2:
        if not data.get(x):
            data[x] = data2[x]
    # ---
    study_id_dir = get_study_dir(study_id)
    file = study_id_dir / "names.json"
    # ---
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            printe.output(f"<<green>> write {len(data)} to file: {file}")

    except Exception as e:
        printe.output(f"<<red>> Error writing to file {file}: {str(e)}")
    # ---
    new_data = [{"url": url, "urlid": "", "file": file} for url, file in data.items()]
    # ---
    insert_all_infos(new_data, prnt=False)


def get_cach(study_id):
    # ---
    # file = studies_names_dir / f"{study_id}.json"
    # ---
    study_id_dir = get_study_dir(study_id)
    # ---
    file = study_id_dir / "names.json"
    # ---
    if file.exists():
        printe.output(f"<<green>> get_cach: {file} exists")
        with open(file, encoding="utf-8") as f:
            return json.load(f)
    # ---
    return {}


def get_file_name(url, url_to_file, study_id):
    # ---
    data_uu.setdefault(study_id, {})
    # ---
    file_name = ""
    # ---
    file_name = find_file_name_from_url(url, do_api=False)
    # ---
    if file_name:
        data_uu[study_id][url] = file_name
    # ---
    if "oo" in sys.argv:
        # # ---
        if not file_name:
            file_name = url_to_file.get(url)
        # # ---
        if not file_name:
            file_name = from_sf_infos(url, study_id)
    # ---
    if not file_name and "noapi" not in sys.argv:
        file_name = find_file_name_from_url(url, do_api=True)
        # if file_name:
        data_uu[study_id][url] = file_name
    # ---
    return file_name


def find_from_data_db(url, urlid):
    # ---
    if "nodb" in sys.argv:
        return ""
    # ---
    data = find_data(url=url, urlid=urlid, file="")
    # ---
    if not data:
        return ""
    # ---
    if len(data) == 1:
        return data[0]["file"]
    # ---
    for d in data:
        if d["url"] == url and d["file"]:
            return d["file"]
    # ---
    return ""


def get_files_names(urls, url_to_file, study_id):
    # ---
    if study_id not in data_uu:
        data_uu[study_id] = {}
    # ---
    cach = get_cach(study_id)
    # ---
    files_names = {}
    # ---
    url_data2 = get_file_urls_new(study_id)
    # ---
    url_data_to_file = {d["url"]: file for file, d in url_data2.items() if d.get("url")}
    # ---
    rev_id_to_file = {d["id"]: file for file, d in url_data2.items() if d.get("id")}
    # ---
    for url in tqdm.tqdm(urls):
        # ---
        # printe.output(f"<<yellow>> get_files_names: {n}/{len(urls)}: {url}")
        # ---
        url_id = ""
        # ---
        # find id from url like: https://prod-images-static.radiopaedia.org/images/(\d+)/.*?$
        mat = re.match(r"https://prod-images-static.radiopaedia.org/images/(\d+)/.*?$", url)
        if mat:
            url_id = mat.group(1)
        # ---
        file_name = cach.get(url)
        # ---
        if not file_name:
            file_name = find_from_data_db(url, url_id)
            if file_name:
                printe.output(f"<<green>> find_from_data_db: {url} -> {file_name}")
        # ---
        if not file_name:
            file_name = url_data_to_file.get(url, "")
        # ---
        if not file_name and url_id:
            file_name = rev_id_to_file.get(url_id, "")
        # ---
        if not file_name and url_id:
            file_name = get_images_ids(img_id=url_id)
        # ---
        if not file_name:
            file_name = get_file_name(url, url_to_file, study_id)
        # ---
        if file_name and not file_name.startswith("File:"):
            file_name = "File:" + file_name
        # ---
        files_names[url] = file_name
    # ---
    if data_uu[study_id]:
        dump_it(data_uu[study_id], cach, study_id)
    # ---
    return files_names
