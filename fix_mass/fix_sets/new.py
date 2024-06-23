"""

tfj run cdcf --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/o updatetex 90505 nodone noid noc del2 multi"

python3 core8/pwb.py fix_mass/fix_sets/new ask 109711 # 2files
python3 core8/pwb.py fix_mass/fix_sets/new ask 143304
python3 core8/pwb.py fix_mass/fix_sets/new ask 80304 printtext
python3 core8/pwb.py fix_mass/fix_sets/new ask 14038 printtext
python3 core8/pwb.py fix_mass/fix_sets/new ask 62191 printtext
python3 core8/pwb.py fix_mass/fix_sets/new ask
python3 core8/pwb.py fix_mass/fix_sets/new ask
python3 core8/pwb.py fix_mass/fix_sets/new ask 71160
python3 core8/pwb.py fix_mass/fix_sets/new ask 80302
python3 core8/pwb.py fix_mass/fix_sets/new ask 14090
python3 core8/pwb.py fix_mass/fix_sets/new ask all
"""
# import re
import sys
from newapi import printe
from newapi.ncc_page import MainPage as ncc_MainPage

from fix_mass.fix_sets.bots.stacks import get_stacks  # get_stacks(study_id)
from fix_mass.fix_sets.bots.has_url import has_url_append

from fix_mass.fix_sets.bots2.text_cat_bot import add_cat_to_set, fix_cats
from fix_mass.fix_sets.bots2.filter_ids import filter_no_title, filter_done
from fix_mass.fix_sets.bots2.set_text2 import make_text_study
from fix_mass.fix_sets.bots2.move_files2 import to_move_work
# from fix_mass.fix_sets.bots2.done2 import find_done_study  # find_done_study(title)

from fix_mass.jsons.files import studies_titles, studies_titles2

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
    if p_text.find("[[Category:Radiopaedia case ") == -1:
        n_text = add_cat_to_set(n_text, study_id, title)
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
    json_data = get_stacks(study_id)
    # ---
    all_files = []
    # ---
    for x in json_data:
        all_files.extend([x["public_filename"] for x in x["images"]])
    # ---
    all_files = list(set(all_files))
    # ---
    printe.output(f"all_files: {len(all_files)}")
    # ---
    if len(all_files) < 3:
        printe.output(f"\t\t<<lightred>>SKIP: <<yellow>> {study_id=}, all_files < 3")
        return "", {}
    # ---
    text, to_move = make_text_study(json_data, study_title, study_id)
    # ---
    return text, to_move


def work_one_study(study_id, study_title=""):
    # ---
    if not study_title:
        study_title = studies_titles.get(study_id) or studies_titles2.get(study_id)
    # ---
    if not study_title:
        printe.output(f"<<red>> study_title is empty... study_id: {study_id}")
        return
    # ---
    printe.output(f"_____________\n {study_id=}, {study_title=}")
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
    ids_titles = filter_no_title(ids)
    # ---
    ids_titles = filter_done(ids_titles)
    # ---
    for study_id, study_title in ids_titles.items():
        work_one_study(study_id, study_title)


if __name__ == "__main__":
    ids = [arg.strip() for arg in sys.argv if arg.strip().isdigit()]
    # ---
    main(ids)
