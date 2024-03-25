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
from mass.radio.authors_list.auths_infos import get_author_infos

# ---
main_dir = Path(__file__).parent.parent
# ---
with open(os.path.join(str(main_dir), 'authors_list/authors_to_cases.json'), 'r', encoding='utf-8') as f:
    authors_to_cases = json.load(f)
# ---
with open(os.path.join(str(main_dir), 'authors_list/authors_infos.json'), 'r', encoding='utf-8') as f:
    authors_infos = json.load(f)
# ---
with open(os.path.join(str(main_dir), 'jsons/all_ids.json'), 'r', encoding='utf-8') as f:
    all_ids = json.load(f)
# ---
print(f"Length of all_ids: {len(all_ids)}")
print(f"Length of authors_to_cases: {len(authors_to_cases)}")
print(f"Length of authors_infos: {len(authors_infos)}")
# ---


def make_authors_infos():
    # ---
    auths_infos = authors_infos.copy()
    # ---
    for numb, x in enumerate(authors_to_cases.keys(), start=1):
        # ---
        done = auths_infos[x]["url"] and auths_infos[x]["location"]
        # ---
        if done:
            printe.output(f"Skip {x} done..")
            continue
        # ---
        first_case = authors_to_cases[x][0]
        first_case_url = all_ids.get(first_case, {}).get('url', None)
        # ---
        auths_infos[x] = get_author_infos(x, first_case_url)
        auths_infos[x]["cases"] = len(authors_to_cases[x])
        # ---
        if "break" in sys.argv and numb % 10 == 0:
            break
    # ---
    if "nodump" not in sys.argv:
        with open(os.path.join(str(main_dir), 'authors_list/authors_infos.json'), 'w', encoding='utf-8') as f:
            json.dump(auths_infos, f, ensure_ascii=False, indent=4)


def start():
    make_authors_infos()


if __name__ == '__main__':
    start()
