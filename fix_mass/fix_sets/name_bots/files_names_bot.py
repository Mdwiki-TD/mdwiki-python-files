"""

from fix_mass.fix_sets.name_bots.files_names_bot import get_files_names

"""
import re
import json
import tqdm
import sys
from newapi import printe

from fix_mass.fix_sets.name_bots.db_duplict_bot import find_url_file_upload
from fix_mass.fix_sets.name_bots.get_rev import get_file_urls_rev  # get_file_urls_rev(study_id)

# from fix_mass.fix_sets.lists.sf_infos import from_sf_infs  # from_sf_infs(url, study_id)
from fix_mass.fix_sets.jsons_dirs import get_study_dir

from fix_mass.dp_infos.db_duplict import insert_all_infos
from fix_mass.file_infos.db import find_from_data_db  # find_from_data_db(url, urlid)

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
    # ---
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


def get_names_from_cach(study_id):
    # ---
    study_id_dir = get_study_dir(study_id)
    # ---
    file = study_id_dir / "names.json"
    # ---
    if file.exists():
        printe.output(f"<<green>> get_names_from_cach: {file} exists")
        with open(file, encoding="utf-8") as f:
            return json.load(f)
    # ---
    return {}


def get_file_name_dd(url, study_id, url_data_to_file, rev_id_to_file):
    # ---
    data_uu.setdefault(study_id, {})
    # ---
    if url in data_uu.get(study_id, {}):
        return data_uu[study_id][url]
    # ---
    url_id = ""
    # ---
    # find id from url like: https://prod-images-static.radiopaedia.org/images/(\d+)/.*?$
    mat = re.match(r"https://prod-images-static.radiopaedia.org/images/(\d+)/.*?$", url)
    if mat:
        url_id = mat.group(1)
    # ---
    file_name = ""
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
    if not file_name:
        do_api = "noapi" not in sys.argv
        file_name = find_url_file_upload(url, do_api=do_api)
    # ---
    data_uu[study_id][url] = file_name
    # ---
    return file_name


def get_file_name_no_dd(url, url_to_file):
    file_name = ""
    # ---
    if not file_name:
        if "oo" in sys.argv:
            file_name = url_to_file.get(url)
    # ---
    # if not file_name: file_name = from_sf_infs(url, study_id)
    # ---
    return file_name


def get_files_names(urls, url_to_file, study_id):
    # ---
    if study_id not in data_uu:
        data_uu[study_id] = {}
    # ---
    cach = get_names_from_cach(study_id)
    # ---
    url_data2 = get_file_urls_rev(study_id)
    # ---
    url_data_to_file = {d["url"]: file for file, d in url_data2.items() if d.get("url")}
    # ---
    rev_id_to_file = {d["id"]: file for file, d in url_data2.items() if d.get("id")}
    # ---
    files_names = {}
    # ---
    for url in tqdm.tqdm(urls):
        # ---
        # printe.output(f"<<yellow>> get_files_names: {n}/{len(urls)}: {url}")
        # ---
        file_name = cach.get(url)
        # ---
        if not file_name:
            file_name = get_file_name_dd(url, study_id, url_data_to_file, rev_id_to_file)
        # ---
        if not file_name:
            file_name = get_file_name_no_dd(url, url_to_file)
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
