"""

tfj run onebot --image python3.9 --command "$HOME/pybot/fix_mass/one_img_cat/u.sh"
tfj run onebot --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/one_img_cat/bot"

python3 core8/pwb.py fix_mass/one_img_cat/bot from_files ask three
python3 core8/pwb.py fix_mass/one_img_cat/bot files ask
python3 core8/pwb.py fix_mass/one_img_cat/bot ask

إضافة تصنيف إلى الصفحات التي بها صورة واحدة فقط

"""
import json
import tqdm
import sys
from pathlib import Path
from newapi import printe
from newapi.ncc_page import MainPage as ncc_MainPage
from newapi.ncc_page import CatDepth

from fix_mass.fix_sets.bots2.filter_ids import filter_no_title
from fix_mass.fix_sets.bots.stacks import get_stacks
from fix_mass.fix_sets.jsons_dirs import st_ref_infos
from fix_mass.jsons.files import studies_titles

Dir = Path(__file__).parent

MAIN_CAT_ONE = "Category:Radiopaedia sets one image"
MAIN_COUNT = 1
args_na = {
    "2": "Category:Radiopaedia sets two images",
    "3": "Category:Radiopaedia sets three images",
    "4": "Category:Radiopaedia sets four images",
    "5": "Category:Radiopaedia sets five images",
    "6": "Category:Radiopaedia sets six images",
    "7": "Category:Radiopaedia sets seven images",
    "8": "Category:Radiopaedia sets eight images",
    "9": "Category:Radiopaedia sets nine images",
    "10": "Category:Radiopaedia sets ten images",
    "xxxx": "Category:Radiopaedia sets > 50 images",
    "50": "Category:Radiopaedia sets more than 50 images",
    "100": "Category:Radiopaedia sets more than 100 images",
    "200": "Category:Radiopaedia sets more than 200 images",
    "500": "Category:Radiopaedia sets more than 500 images",
    "1000": "Category:Radiopaedia sets more than 1000 images",
    "1500": "Category:Radiopaedia sets more than 1500 images",
    "2000": "Category:Radiopaedia sets more than 2000 images",
}
args_na_more = {
    50: 100,
    100: 500,
    500: 1000,
    1000: 1500,
    1500: 2000,
    2000: 3000,
}

count_cach = {}

for x, ba in args_na.items():
    if x in sys.argv:
        MAIN_COUNT = int(x)
        MAIN_CAT_ONE = ba
        printe.output(f"<<yellow>> MAIN_CAT_ONE: {MAIN_CAT_ONE}, MAIN_COUNT: {MAIN_COUNT}")
        break


def update_text(title):
    # ---
    printe.output(f"<<yellow>> update_text: {title}")
    # ---
    page = ncc_MainPage(title, "www", family="nccommons")
    # ---
    p_text = page.get_text()
    new_text = p_text
    # ---
    for x in args_na.values():
        x_in = f"[[{x}]]"
        if new_text.find(x_in) != -1:
            new_text = new_text.replace(x_in, "")
    # ---
    if new_text.find(MAIN_CAT_ONE) == -1:
        new_text += f"\n[[{MAIN_CAT_ONE}]]"
    # ---
    if new_text.strip() == p_text.strip():
        printe.output("no changes..")
        return
    # ---
    page.save(newtext=new_text, summary=f"Added [[:{MAIN_CAT_ONE}]]")


def count_files(study_id):
    # ---
    study_id = str(study_id)
    # ---
    if count_cach.get(study_id):
        return count_cach[study_id]
    # ---
    stacks_data = get_stacks(study_id)
    # ---
    all_files = []
    # ---
    for x in stacks_data:
        all_files.extend([x["public_filename"] for x in x["images"]])
    # ---
    all_files = list(set(all_files))
    # ---
    count_cach[study_id] = len(all_files)
    # ---
    return len(all_files)


def count_files_true(k, main_number, counts=False):
    # ---
    if not counts:
        counts = count_files(k)
    # ---
    if main_number in args_na_more:
        if counts >= main_number and counts < args_na_more[main_number]:
            return True
    else:
        if counts == main_number:
            return True
    # ---
    return False


def from_files_g(files_file):
    # ---
    if not files_file.exists():
        files_file.write_text("{}")
    # ---
    if "from_files" not in sys.argv:
        return False
    # ---
    try:
        with open(files_file, "r", encoding="utf-8") as f:
            lisst_of_s = json.load(f)
    except Exception as e:
        printe.output(f"<<red>> Error reading {files_file}: {str(e)}")
        return False
    # ---
    if lisst_of_s:
        for x, counts in lisst_of_s.items():
            count_cach[x] = counts
    # ---
    return lisst_of_s


def from_files():
    lisst_of_s = []
    # ---
    files_file = Dir / "studies_one_file.json"
    # ---
    da = from_files_g(files_file)
    if da:
        return da
    # ---
    for subdir in tqdm.tqdm(st_ref_infos.iterdir(), total=80000):
        # ---
        if not subdir.is_dir():
            continue
        # ---
        study_id = subdir.name
        # ---
        file_js = subdir / "stacks.json"
        # ---
        if not file_js.exists():
            continue
        # ---
        lisst_of_s.append(study_id)
    # ---
    lisst_of_s = {x: count_files(x) for x in lisst_of_s}
    # ---
    with open(files_file, "w", encoding="utf-8") as f:
        json.dump(lisst_of_s, f, ensure_ascii=False, indent=2)
    # ---
    return lisst_of_s


def main():
    # ---
    if "files" in sys.argv or "from_files" in sys.argv:
        ids = from_files()
        printe.output(f"<<yellow>> ids from_files: {len(ids):,}")
        ids_titles = filter_no_title(ids)
    else:
        ids_titles = studies_titles.copy()
        printe.output(f"<<yellow>> ids from studies_titles: {len(ids_titles):,}")
    # ---
    print("work on count files:")
    # ---
    ids_titles = {k: v for k, v in ids_titles.items() if count_files_true(k, MAIN_COUNT)}
    # ---
    printe.output(f"<<yellow>> titles_only_one: {len(ids_titles):,}")
    printe.output(f"<<yellow>> titles_only_one: {len(ids_titles):,}")
    printe.output(f"<<yellow>> titles_only_one: {len(ids_titles):,}")
    # ---
    if not ids_titles:
        printe.output("<<red>> no ids_titles")
        return
    # ---
    pages_in = CatDepth(MAIN_CAT_ONE, sitecode="www", family="nccommons", depth=0, only_titles=True)
    # ---
    ids_titles = {s_id: s_t for s_id, s_t in ids_titles.items() if s_t not in pages_in.keys()}
    # ---
    printe.output(f"<<green>> ids_titles: {len(ids_titles):,}, after remove already_done..")
    # ---
    if not ids_titles:
        printe.output("<<red>> no ids_titles")
        return
    # ---
    cat_page = ncc_MainPage(MAIN_CAT_ONE, "www", family="nccommons")
    # ---
    if not cat_page.exists():
        printe.output(f"<<red>> {MAIN_CAT_ONE} not exists")
        cat_page.Create(f"[[Category:Radiopaedia sets by number of images|{MAIN_COUNT}]]")
    # ---
    for n, (study_id, study_title) in enumerate(ids_titles.items()):
        # ---
        printe.output(f"page: {n}/{len(ids_titles):,}:")
        # printe.output(f"{study_id=}, {study_title=}")
        # ---
        all_files = count_files(study_id)
        # ---
        # printe.output(f"all_files: {all_files}")
        # ---
        # if all_files != MAIN_COUNT:
        if not count_files_true(study_id, MAIN_COUNT, counts=all_files):
            continue
        # ---
        update_text(study_title)


if __name__ == "__main__":
    main()
