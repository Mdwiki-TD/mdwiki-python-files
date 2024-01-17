# -*- coding: utf-8 -*-
"""
python3 core8/pwb.py mass/radio/all_cats ask

"""
import os
import json
from pathlib import Path
from new_api.ncc_page import MainPage as ncc_MainPage

# Specify the root folder
main_dir = Path(__file__).parent


def doo():
    with open(os.path.join(str(main_dir), 'jsons/ids.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)

    text = '{| class="wikitable sortable"\n|-\n'
    text += '! # !! Category !! Image set\n|-\n'
    n = 0

    for _, tab in data.items():
        caseId = tab['caseId']
        title = tab['title']
        category = f'Radiopaedia case {caseId} {title}'
        n += 1
        text += f'! {n}\n'
        text += f'| [[:Category:{category}]]\n'
        text += f'| [[{category}]]\n'
        text += '|-\n'

    text += '|}'
    text += '\n[[Category:Radiopaedia|*]]'

    page = ncc_MainPage('User:Mr._Ibrahem/Radiopaedia', 'www', family='nccommons')
    # ---
    page.save(newtext=text, summary='update', nocreate=0, minor='')
    # sort names by count


if __name__ == "__main__":
    # Process all subfolders in the specified root folder
    doo()
