"""

python3 core8/pwb.py fix_mass/dp_infos/add_duplict
python3 core8/pwb.py fix_mass/dp_infos/add_duplict names

"""
import sys
import tqdm
import json
from pathlib import Path
from fix_mass.fix_sets.jsons_dirs import st_ref_infos
from fix_mass.dp_infos.db_duplict import insert_all_infos  # , insert_url_file  # insert_url_file(url, file)

Dir = Path(st_ref_infos)

# list of subdirs in st_ref_infos
# subdirs = [x for x in Dir.iterdir() if x.is_dir()]


def work(na="names"):
    lisst_of_files = []
    na = na if na in ["names", "rev"] else "names"

    for subdir in tqdm.tqdm(Dir.iterdir(), total=80000):
        # ---
        if not subdir.is_dir():
            continue
        # ---
        # find "names.json"
        # file_js = subdir / "names.json"
        file_js = subdir / f"{na}.json"
        # ---
        if not file_js.exists():
            continue
        # ---
        lisst_of_files.append(file_js)
    # ---
    for file_js in tqdm.tqdm(lisst_of_files):
        # ---
        with open(file_js, encoding="utf-8") as f:
            data = json.load(f)
        # ---
        # print(f"{file_js}, len(data): {len(data)}")
        # ---
        for i in range(0, len(data), 100):
            group = dict(list(data.items())[i : i + 100])
            # ---
            if na == "names":
                new_data = [{"url": url, "urlid": "", "file": file} for url, file in group.items()]
            else:
                new_data = [{"url": da["url"], "urlid": da["id"], "file": file} for file, da in group.items()]
            # ---
            insert_all_infos(new_data, prnt=False)


if __name__ == "__main__":
    na = "names" if "names" in sys.argv else "rev"
    work(na)
