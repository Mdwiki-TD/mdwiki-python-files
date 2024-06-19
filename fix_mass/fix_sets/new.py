"""

tfj run cdcf --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/o updatetex 90505 nodone noid noc del2 multi"

python3 core8/pwb.py fix_mass/fix_sets/new ask 143304
python3 core8/pwb.py fix_mass/fix_sets/new ask 80304 printtext
python3 core8/pwb.py fix_mass/fix_sets/new ask 14038 printtext
python3 core8/pwb.py fix_mass/fix_sets/new ask
python3 core8/pwb.py fix_mass/fix_sets/new ask
python3 core8/pwb.py fix_mass/fix_sets/new ask
python3 core8/pwb.py fix_mass/fix_sets/new ask 71160
python3 core8/pwb.py fix_mass/fix_sets/new ask 80302
python3 core8/pwb.py fix_mass/fix_sets/new ask 14090
python3 core8/pwb.py fix_mass/fix_sets/new ask all
"""
import sys
from newapi import printe
from newapi.ncc_page import MainPage as ncc_MainPage

from fix_mass.fix_sets.bots.get_img_info import one_img_info
from fix_mass.fix_sets.bots.stacks import get_stacks  # get_stacks(study_id)
from fix_mass.fix_sets.bots2.set_text2 import make_text_study
from fix_mass.fix_sets.bots.study_files import get_study_files
from fix_mass.fix_sets.bots2.move_files2 import to_move_work
from fix_mass.jsons.files import studies_titles  # , studies_titles2
from fix_mass.fix_sets.bots.has_url import has_url_append
from fix_mass.fix_sets.bots2.done2 import find_done_study  # find_done_study(title)

def fix_cats(text, p_text):
    cat_text = ""
    # ---
    if p_text.find("[[Category:") != -1:
        cat_text = "[[Category:" + p_text.split("[[Category:", maxsplit=1)[1]
    # ---
    text = text.strip()
    # ---
    cat_list = [x.strip() for x in cat_text.split("\n") if x.strip()]
    # ---
    for x in cat_list:
        xtest = x.split("|", maxsplit=1)[0]
        if text.find(xtest) == -1:
            text += f"\n{x}"
    # ---
    return text


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
    # cats = page.get_categories()
    # ---
    # printe.output(cat_text)
    # ---
    # cats_text = "\n".join([f"[[Category:{x}]]" for x in cats])
    # ---
    # cat_text = ""
    # if p_text.find("[[Category:") != -1:
    #     cat_text = "[[Category:" + p_text.split("[[Category:", maxsplit=1)[1]
    # ---
    # n_text += f"\n\n{cat_text}"
    # ---
    n_text += "\n[[Category:Sort studies fixed]]"
    # ---
    n_text = fix_cats(n_text, p_text)
    # ---
    if p_text == n_text:
        printe.output("no changes..")
        return
    # ---
    page.save(newtext=n_text, summary="Fix sort.")


def work_text(study_id, study_title):
    # ---
    files = get_study_files(study_id)
    # ---
    json_data = get_stacks(study_id)
    # ---
    data = one_img_info(files, study_id, json_data)
    # ---
    text, to_move = make_text_study(json_data, data, study_title, study_id)
    # ---
    return text, to_move


def work_one_study(study_id):
    # ---
    study_title = studies_titles.get(study_id)  # or studies_titles2.get(study_id)
    # ---
    printe.output(f"study_id: {study_id}, study_title: {study_title}")
    # ---
    if not study_title:
        printe.output(f"<<red>> study_title for: {study_id=} not found")
        return
    # ---
    if find_done_study(study_title):
        printe.output(f"<<purple>> {study_id=}, ({study_title}) already done, add 'nodone' to sys.argv")
        if "nodone" not in sys.argv:
            return
    # ---
    text, to_move = work_text(study_id, study_title)
    # ---
    text = text.strip()
    # ---
    if text.find("|http") != -1:
        printe.output(f"<<red>> text has http links... study_id: {study_id}")
        has_url_append(study_id)
        if "printtext" in sys.argv:
            printe.output(text)
        return
    # ---
    if not text:
        printe.output(f"<<red>> text is empty... study_id: {study_id}")
        return
    # ---
    text = to_move_work(text, to_move, study_id)
    # ---
    update_set_text(study_title, text, study_id)


def main(ids):
    # ---
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    # ---
    for study_id in ids:
        work_one_study(study_id)


if __name__ == "__main__":
    ids = [arg.strip() for arg in sys.argv if arg.strip().isdigit()]
    # ---
    main(ids)
