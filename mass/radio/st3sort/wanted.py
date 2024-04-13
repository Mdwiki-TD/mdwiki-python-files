"""
tfj run wanted --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/wanted nomulti unused"

python3 core8/pwb.py mass/radio/st3/wanted nomulti unused ask
python3 core8/pwb.py mass/radio/st3/wanted nomulti ask
python3 core8/pwb.py mass/radio/st3/wanted nomulti add_category

"""
import sys
import re

# ---
from newapi.ncc_page import NEW_API
from mass.radio.st3sort.start3 import main_by_ids

# ---
api_new = NEW_API('www', family='nccommons')
api_new.Login_to_wiki()
# ---


def titles_to_ids(titles):
    cases = []
    # ---
    reg = r'^Category:Radiopaedia case (\d+) (.*?)$'
    # ---
    for cat in titles:
        match = re.match(reg, cat)
        if match:
            case_id = match.group(1)
            cases.append(case_id)
    # ---
    return cases


# ---
prop = "Wantedcategories"
# ---
if "unused" in sys.argv:
    prop = "Unusedcategories"
# ---
# Unusedcategories: { "ns": 14, "title": "Category:Radiopaedia case 10033 Congenital diaphragmatic hernia" }
# Wantedcategories:{'value': '823', 'ns': 14, 'title': 'Category:Radiopaedia case 154144 Primary CNS lymphoma-atypical cortical location'}
# ---
cats = api_new.querypage_list(qppage=prop, qplimit="max", Max=5000)
# ---
cats = [x['title'] for x in cats]
# ---
print(f"len cats: {len(cats)}")
# ---
wanted_ids = titles_to_ids(cats)
# ---
main_by_ids(wanted_ids)
