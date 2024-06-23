"""
from fix_mass.fix_sets.bots2.text_cat_bot import add_cat_to_set, fix_cats
"""

import re
from fix_mass.jsons.files import study_to_case_cats, study_id_to_case_id

from mass.radio.jsons_files import jsons
# ---
cases_cats_list = jsons.cases_cats.copy()
# ---

def add_cat_to_set(p_text, study_id, title):
    # ---
    case_id = ""
    # ---
    # match text like (Radiopaedia 84641-100054
    ma = re.search(r"\(Radiopaedia (\d+)-(\d+) ", title)
    if ma:
        case_id = ma.group(1)
    # ---
    if not case_id:
        case_id = study_id_to_case_id.get(study_id)
    # ---
    cat = study_to_case_cats.get(study_id) or (cases_cats_list.get(case_id) if case_id else "")
    # ---
    if not cat:
        print(f"no cat for {study_id=}")
        return p_text
    # ---
    if p_text.find(cat) != -1:
        print(f"page has {cat=}")
        return p_text
    # ---
    match_cats = re.findall(r"\[\[(Category:.*?)\]\]", p_text)
    # ---
    if not match_cats:
        print(f"no match for {study_id=}")
        return p_text
    # ---
    for x in match_cats:
        if x.find(case_id) != -1 or (x.find(study_id) != -1 if study_id else False):
            print(f"page has {case_id=} in {x=}")
            return p_text
    # ---
    p_text += f"\n[[{cat}]]"
    # ---
    return p_text


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
