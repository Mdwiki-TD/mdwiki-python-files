"""

python3 core8/pwb.py fix_mass/fix_sets/fix 134732

"""
import json
import sys
from pathlib import Path
from newapi import printe

from fix_mass.fix_sets.bots.get_img_info import one_img_info
from fix_mass.fix_sets.bots.stacks import get_stacks  # get_stacks(study_id)
from fix_mass.fix_sets.bots.set_text import make_text_one_study
from fix_mass.fix_sets.bots.study_files import get_study_files
from fix_mass.fix_sets.bots.mv_files import to_move_work
from fix_mass.fix_sets.jsons.files import studies_titles, study_to_case_cats

from newapi.ncc_page import MainPage as ncc_MainPage

main_dir = Path(__file__).parent


def update_set_text(title, n_text):
    # ---
    page = ncc_MainPage(title, "www", family="nccommons")
    # ---
    p_text = page.get_text()
    # ---
    # split p_text get after first [[Category:
    # ---
    cat_text = "[[Category:" + p_text.split("[[Category:", maxsplit=1)[1]
    # ---
    # cats = page.get_categories()
    # # ---
    printe.output(cat_text)
    # # ---
    # cats_text = "\n".join([f"[[Category:{x}]]" for x in cats])
    # ---
    n_text += f"\n\n{cat_text}"
    # ---
    if p_text != n_text:
        page.save(newtext=n_text, summary="update")


def work_text(study_id, study_title):
    files = get_study_files(study_id)
    # ---
    data = one_img_info(files, study_id)
    # ---
    # 'File:Appendicitis (CT angiogram) (Radiopaedia 154713-134732 This comic explains the pathophysiology of appendicitis. 1).jpg': {'img_url': 'https://prod-images-static.radiopaedia.org/images/61855971/f11ad965ab35e44ae8ac9ed236afb1cf4547507d8f464cbc3c6316a4cb76fb32.jpg', 'case_url': 'https://radiopaedia.org/cases/appendicitis-ct-angiogram', 'study_url': 'https://radiopaedia.org/cases/154713/studies/134732', 'caseId': '154713', 'studyId': '134732'}
    # printe.output(data)
    # ---
    url_to_file = {v["img_url"]: x for x, v in data.items()}
    # ---
    # printe.output(json.dumps(url_to_file, indent=2))
    # ---
    json_data = get_stacks(study_id)
    # ---
    text, to_move = make_text_one_study(json_data, url_to_file, study_title)
    # ---
    return text, to_move


def work_one_study(study_id):
    # one_img_info
    # ---
    study_title = studies_titles.get(study_id, "")
    # ---
    printe.output(f"study_id: {study_id}, study_title: {study_title}")
    # ---
    text, to_move = work_text(study_id, study_title)
    # ---
    text = to_move_work(text, to_move)
    # ---
    update_set_text(study_title, text)
    # ---


def main(ids):
    # ---
    for study_id in ids:
        work_one_study(study_id)


if __name__ == "__main__":
    ids = [arg for arg in sys.argv[1:] if arg.isdigit()]
    main(ids)
