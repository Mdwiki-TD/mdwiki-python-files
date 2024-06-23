"""

tfj run cdcf --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/o updatetex 90505 nodone noid noc del2 multi"
tfj run catpages --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/set_cats catpages"

python3 core8/pwb.py fix_mass/fix_sets/set_cats catpages ask
python3 core8/pwb.py fix_mass/fix_sets/set_cats studies_titles2 ask

"""
import tqdm
import re
import sys
from newapi import printe
from newapi.ncc_page import MainPage as ncc_MainPage
from newapi.ncc_page import CatDepth

from fix_mass.fix_sets.bots2.text_cat_bot import add_cat_to_set
from fix_mass.fix_sets.bots2.filter_ids import filter_no_title
from fix_mass.jsons.files import studies_titles, studies_titles2


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
    page = ncc_MainPage(study_title, "www", family="nccommons")
    # ---
    p_text = page.get_text()
    # ---
    if p_text.find("[[Category:Radiopaedia case ") != -1:
        printe.output("page has cat.")
        return
    # ---
    n_text = p_text
    # ---
    n_text = add_cat_to_set(n_text, study_id, study_title)
    # ---
    if n_text == p_text:
        printe.output("no changes..")
        return
    # ---
    page.save(newtext=n_text, summary="Add cat.")


def cat_pages():
    cat1 = CatDepth("Category:Image set", sitecode="www", family="nccommons", depth=0)
    cat2 = CatDepth("Category:Radiopaedia sets", sitecode="www", family="nccommons", depth=0)
    # ---
    # new_list = cat1 items not in cat2 items
    new_list = list(set(cat1) - set(cat2))
    # ---
    for title in tqdm.tqdm(new_list):
        # ---
        # match text like (Radiopaedia 84641-100054
        ma = re.search(r"\(Radiopaedia (\d+)-(\d+) ", title)
        if ma:
            study_id = ma.group(2)
            # ---
            work_one_study(study_id, title)


def main(ids):
    # ---
    if not ids:
        ids = list(studies_titles.keys())
        # ---
        if "studies_titles2" in sys.argv:
            ids = list(studies_titles2.keys())
    # ---
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    # ---
    ids_titles = filter_no_title(ids)
    # ---
    for study_id, study_title in ids_titles.items():
        work_one_study(study_id, study_title)


if __name__ == "__main__":
    ids = [arg.strip() for arg in sys.argv if arg.strip().isdigit()]
    # ---
    if "catpages" in sys.argv:
        cat_pages()
    else:
        main(ids)
