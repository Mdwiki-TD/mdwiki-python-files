'''

$HOME/local/bin/python3 core8/pwb.py mass/radio/authors_list/save

'''
import re
import sys
import json
import os
from pathlib import Path

# ---
from newapi.ncc_page import MainPage as ncc_MainPage

# ---
main_dir = Path(__file__).parent.parent
# ---
with open(os.path.join(str(main_dir), 'authors_list/authors_infos.json'), "r", encoding="utf-8") as f:
    authors_infos = json.load(f)
# ---


def sa(au_infos):
    text = ""

    text += f"* All Authors: {len(au_infos):,}\n"

    text += '{| class="wikitable sortable"\n'
    text += '|-\n'
    text += '! # !! Author !! cats !! Cases !! Url !! Location\n'

    # sort au_infos by cases
    au_infos = dict(sorted(au_infos.items(), key=lambda x: x[1]["cases"], reverse=True))

    for numb, (x, ta) in enumerate(au_infos.items(), 1):
        text += '|-\n'
        text += f'! {numb}\n'
        text += f'| [[:Category:Radiopaedia cases by {x}|{x}]]\n'
        text += f'| {{{{PAGESINCATEGORY:Radiopaedia cases by {x}}}}}\n'
        text += f'| {ta["cases"]:,}\n'
        text += f'| {ta["url"]}\n'
        text += f'| {ta["location"]}\n'

    text += '|}\n\n'

    page = ncc_MainPage("User:Mr. Ibrahem/Radiopaedia authors", 'www', family='nccommons')

    if page.exists():
        page.save(newtext=text, summary='update')
    else:
        page.Create(text=text, summary='update')


if __name__ == '__main__':
    sa(authors_infos)
