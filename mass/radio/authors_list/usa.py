'''

$HOME/local/bin/python3 core8/pwb.py mass/radio/authors_list/usa nomulti updatetext ask

tfj run usa --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/authors_list/usa nomulti up updatetext"

'''
import re
import sys
import json
from pathlib import Path
# ---
from newapi import printe
from mass.radio.st3.start3 import main_by_ids
# ---
main_dir = Path(__file__).parent
# ---
with open(main_dir / 'authors_infos.json', 'r', encoding='utf-8') as f:
    authors_infos = json.load(f)
# ---
with open(main_dir / 'authors_to_cases.json', 'r', encoding='utf-8') as f:
    authors_to_cases = json.load(f)
# ---

def sa(au_infos):
    print(f"len all authors: {len(au_infos)}")

    # filter only authors with location contains "united states"
    usa_auths = [ k for k, v in au_infos.items() if 'united states' in v['location'].lower()]
    print(f"len usa_auths: {len(usa_auths)}")

    tab = { au : authors_to_cases.get(au, []) for au in usa_auths if au in authors_to_cases}
    print(f"len tab: {len(tab)}")

    # sort by number of cases
    Reverse = "reverse" in sys.argv
    tab = dict(sorted(tab.items(), key=lambda item: len(item[1]), reverse=Reverse))

    
    for numb, (author, ids) in enumerate(tab.items(), 1):
        ids = authors_to_cases.get(author, [])
        printe.output("<<yellow>>=========================")
        printe.output(f"<<yellow>> {numb}: {author=}: {len(ids)=}")

        if "up" not in sys.argv:
            continue

        if ids:
            main_by_ids(ids)

if __name__ == '__main__':
    sa(authors_infos)
