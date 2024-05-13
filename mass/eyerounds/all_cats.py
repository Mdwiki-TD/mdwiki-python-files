# -*- coding: utf-8 -*-
"""
python3 core8/pwb.py mass/eyerounds/all_cats ask

"""
import re
import os
import json
from pathlib import Path
from newapi.ncc_page import MainPage as ncc_MainPage

# Specify the root folder
main_dir = Path(__file__).parent

from mass.eyerounds.bots.url_to_title import urls_to_title
from mass.eyerounds.bots.catbot import category_name

def doo():
    with open(os.path.join(str(main_dir), 'jsons/images.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)

    names = {}
    chapters = {}

    for name, info_data in data.items():
        images_info = info_data.get("images", {})
        if not images_info:
            continue
        chapters[name] = len(images_info.keys())
        # ---
        for u, name in images_info.items():
            if name not in names:
                names[name] = 0
            names[name] += 1

    done = {}

    text = '{| class="wikitable sortable"\n|-\n' + '! # !! Category !! Image set !! Case number !! Url !! Number of images\n|-\n'
    for n, (url, count) in enumerate(chapters.items(), start=1):
        x = urls_to_title.get(url)
        done.setdefault(x, 0)
        done[x] += 1
        cat, numb = category_name(url)
        if not cat:
            cat = f"{x} (EyeRounds)"
        text += f'! {n}\n'
        text += f'| [[:Category:{cat}]]\n'
        text += f'| [[{cat}|set]]\n'  # + '|| {{#ifexist:' + x2 + '|1|0}}\n'
        text += f'| {numb}\n'
        text += f'| [{url} ]\n'  # + '|| {{#ifexist:' + x2 + '|1|0}}\n'
        text += f'| {count}\n'
        text += '|-\n'

    text += '|}'
    text += '\n[[Category:EyeRounds|*]]'

    page = ncc_MainPage('User:Mr._Ibrahem/EyeRounds', 'www', family='nccommons')
    # ---

    # ---
    page.save(newtext=text, summary='update', nocreate=0, minor='')

    # sort names by count
    done = dict(sorted(done.items(), key=lambda x: x[1], reverse=True))

    # print done
    for name, count in done.items():
        if count > 1:
            print(f'{name} {count}')


if __name__ == "__main__":
    # Process all subfolders in the specified root folder
    doo()
