"""

python3 core8/pwb.py fix_mass/fix_sets/fix studies_titles ask
python3 core8/pwb.py fix_mass/fix_sets/fix 134732

"""
import json
import sys
from pathlib import Path
# import xxlimited
from newapi import printe

from fix_mass.fix_sets.bots.get_img_info import one_img_info
from fix_mass.fix_sets.bots.stacks import get_stacks  # get_stacks(study_id)
from fix_mass.fix_sets.bots.set_text import make_text_one_study
from fix_mass.fix_sets.bots.study_files import get_study_files
from fix_mass.fix_sets.bots.mv_files import to_move_work
from fix_mass.fix_sets.jsons.files import studies_titles, studies_titles2
from fix_mass.fix_sets.bots.done import studies_done_append, find_done #find_done(study_id)

from newapi.ncc_page import MainPage as ncc_MainPage

main_dir = Path(__file__).parent


def update_set_text(title, n_text, study_id):
    # ---
    printe.output(f"<<yellow>> update_set_text: {title}")
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
    # printe.output(cat_text)
    # # ---
    # cats_text = "\n".join([f"[[Category:{x}]]" for x in cats])
    # ---
    n_text += f"\n\n{cat_text}"
    # ---
    if p_text != n_text:
        tyy = page.save(newtext=n_text, summary="update")
        # ---
        if tyy:
            studies_done_append(study_id)
        # ---


def work_text(study_id, study_title):
    files = get_study_files(study_id)
    # ---
    json_data = get_stacks(study_id)
    # ---
    data = one_img_info(files, study_id, json_data)
    # ---
    # 'File:Appendicitis (CT angiogram) (Radiopaedia 154713-134732 This comic explains the pathophysiology of appendicitis. 1).jpg': {'img_url': 'https://prod-images-static.radiopaedia.org/images/61855971/f11ad965ab35e44ae8ac9ed236afb1cf4547507d8f464cbc3c6316a4cb76fb32.jpg', 'case_url': 'https://radiopaedia.org/cases/appendicitis-ct-angiogram', 'study_url': 'https://radiopaedia.org/cases/154713/studies/134732', 'caseId': '154713', 'studyId': '134732'}
    # printe.output(data)
    # ---
    # printe.output(json.dumps(url_to_file, indent=2))
    # ---
    text, to_move = make_text_one_study(json_data, data, study_title)
    # ---
    return text, to_move


def work_one_study(study_id):
    # one_img_info
    # ---
    study_title = studies_titles.get(study_id)# or studies_titles2.get(study_id)
    # ---
    if not study_title and "studies_titles2" in sys.argv:
        study_title = studies_titles2.get(study_id)
    # ---
    printe.output(f"study_id: {study_id}, study_title: {study_title}")
    # ---
    if not study_title:
        printe.output(f"<<red>> study_title for: {study_id=} not found")
        return
    # ---
    if find_done(study_id):
        printe.output(f"<<purple>> study_id: {study_id} already done")
        if "nodone" not in sys.argv:
            return
    # ---
    text, to_move = work_text(study_id, study_title)
    # ---
    text = text.strip()
    # ---
    if text.find("|http") != -1:
        printe.output(f"<<red>> text has http links... study_id: {study_id}")
        printe.output(text)
        return
    # ---
    if not text:
        printe.output(f"<<red>> text is empty... study_id: {study_id}")
        return
    # ---
    text = to_move_work(text, to_move)
    # ---
    update_set_text(study_title, text, study_id)
    # ---


def main(ids):
    # ---
    for study_id in ids:
        
        work_one_study(study_id)



if __name__ == "__main__":
    ids = [arg for arg in sys.argv[1:] if arg.isdigit()]
    # ---
    if "studies_titles" in sys.argv:
        # studies_titles keys not in studies_titles2
        # ids = [ x for x in studies_titles.keys() if x not in studies_titles2 ]
        ids = list(studies_titles.keys())
    elif "studies_titles2" in sys.argv:
        ids = [ x for x in studies_titles2.keys() if x not in studies_titles ]
    # ---
    printe.output(f"len of ids: {len(ids)}")
    # ---
    main(ids)
