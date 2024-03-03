'''

python3 core8/pwb.py mass/radio/authors_list/bot1 nodump
python3 core8/pwb.py mass/radio/authors_list/bot1

tfj run auths --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/authors_list/bot1 && $HOME/local/bin/python3 core8/pwb.py mass/radio/authors_list/save"

'''
import re
import sys
import json
import os
from pathlib import Path
from newapi import printe
from newapi.ncc_page import CatDepth
# ---
main_dir = Path(__file__).parent.parent
# ---
with open(os.path.join(str(main_dir), 'authors_list/authors_to_cases.json'), 'r', encoding='utf-8') as f:
    authors_to_cases = json.load(f)
# ---
print(f"Length of authors_to_cases: {len(authors_to_cases)}")
# ---
def cases_cats():
    members = CatDepth('Category:Radiopaedia images by case', sitecode='www', family="nccommons", depth=0, ns="14")
    reg = r'^Category:Radiopaedia case (\d+) (.*?)$'
    # ---
    id2cat = {}
    # ---
    for cat in members:
        match = re.match(reg, cat)
        if match:
            case_id = match.group(1)
            case_title = match.group(2)
            # ---
            id2cat[case_id] = cat
    # ---
    print(f'lenth of members: {len(members)} ')
    print(f'lenth of id2cat: {len(id2cat)} ')
  
    return id2cat


def one_auth(auth, cases_ids, cats):
    # 
def start():
    # ---
    cats = cases_cats()
    for numb, (x, x_cases) in enumerate(authors_to_cases.items(), start=1):
        # ---
        printe.output(f"{x=}, cases: {len(x_cases)=}")
        # ---
        one_auth(auth, cases_ids, cats)
        # ---
        if "break" in sys.argv:
            break
    
if __name__ == '__main__':
    start()
