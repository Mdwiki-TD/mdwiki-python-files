"""
python3 core8/pwb.py fix_mass/dp_infos/fix

"""
import tqdm
import sys
import re
from pathlib import Path

from newapi.db_bot import LiteDB

Dir = Path(__file__).parent

db_path = Dir / "sf_infos_duplict.sqlite"
db_path_new = Dir / "sf_infos_duplict_new.sqlite"

infos_db = LiteDB(db_path)
infos_db_new = LiteDB(db_path_new)

keyys = ["url", "urlid", "file"]

ids_to_urls = {}
ids_to_files = {}
files_to_ids = {}

main_urlid_table = {}


def delete():
    sql = "delete from infos where urlid = '' and url = ''"
    infos_db.update(sql)


def fix():
    duplict_row = 0
    duplict_id = 0
    # ---
    no_urlid = 0
    added_url = 0
    added_file = 0
    # ---
    # Retrieve data
    data = infos_db.get_data("infos")
    # ----
    dup_ids = []
    # ----
    data = [x for x in data]
    # ----
    for row in tqdm.tqdm(data):
        # {'id': 684, 'url': '', 'urlid': '53564408', 'file': 'File:Colonic pseudo-obstruction (Radiopaedia 82485-96627 A 175).jpg'}
        # print(row)
        # ---
        row_id = row["id"]
        del row["id"]
        # ---
        url = row["url"] or ""
        urlid = row["urlid"] or ""
        file = row["file"] or ""
        # ---
        if urlid:
            if urlid not in main_urlid_table:
                main_urlid_table[urlid] = row
            elif main_urlid_table[urlid] == row:
                duplict_row += 1
                dup_ids.append(dup_ids)
            else:
                duplict_id += 1
                # for k, v in row.items():
                #     if not main_urlid_table[urlid].get(k):
                #         main_urlid_table[urlid][k] = v
        else:
            no_urlid += 1
            # print(row)
        # ---
        if urlid and url:
            ids_to_urls[urlid] = url
        # ---
        if urlid and file:
            ids_to_files[urlid] = file
            files_to_ids[file] = urlid
    # ----
    for urlid, dat in tqdm.tqdm(main_urlid_table.copy().items()):
        url = dat["url"]
        file = dat["file"]
        # ---
        if not url and urlid in ids_to_urls:
            main_urlid_table[urlid]["url"] = ids_to_urls[urlid]
            added_url += 1
        # ---
        if not file and urlid in ids_to_files:
            main_urlid_table[urlid]["file"] = ids_to_files[urlid]
            added_file += 1
    # ----
    print(f"len of sql data: {len(data)}")
    print(f"len of new data: {len(main_urlid_table)}")
    # ---
    print(f"duplict_id: {duplict_id}")
    print(f"duplict_row: {duplict_row}")
    print(f"dup_ids: {len(dup_ids)}")
    print(f"added_url: {added_url}, added_file: {added_file}")
    # ---
    print(f"no_urlid: {no_urlid}")
    # ---
    if "new" in sys.argv:
        lista = []
        # ---
        for urlid, dat in tqdm.tqdm(main_urlid_table.copy().items()):
            row = {"url": dat["url"], "urlid": urlid, "file": dat["file"]}
            lista.append(row)
        # ---
        for i in tqdm.tqdm(range(0, len(lista), 1000)):
            rows = lista[i : i + 1000]
            infos_db_new.insert_all("infos", rows, prnt=False)


if __name__ == "__main__":
    if "delete" in sys.argv:
        delete()
    else:
        fix()
