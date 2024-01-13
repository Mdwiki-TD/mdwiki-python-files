'''

python3 core8/pwb.py stats/o

'''
import json
import re
import os
import sys
from pathlib import Path
# ---
from mdpy import printe
from new_api.mdwiki_page import MainPage as md_MainPage
from stats.editors import get_editors
#---
Dir = Path(__file__).parent
sites_dir   = Dir / 'sites'
editors_dir = Dir / 'editors'
#---
change_codes = {
    "nb": "no",
    "bat_smg": "bat-smg",
    "be_x_old": "be-tarask",
    "be-x-old": "be-tarask",
    "cbk_zam": "cbk-zam",
    "fiu_vro": "fiu-vro",
    "map_bms": "map-bms",
    "nds_nl": "nds-nl",
    "roa_rup": "roa-rup",
    "zh_classical": "zh-classical",
    "zh_min_nan": "zh-min-nan",
    "zh_yue": "zh-yue",
}

def work_in_one_site(site, links):
    # ---
    site = re.sub(r'wiki$', '', site)
    # ---
    printe.output(f'<<lightgreen>> site:{site} links: {len(links)}')
    # ---
    if len(links) < 100:
        printe.output('<<red>> less than 100 articles')
        # return
    # ---
    editors = get_editors(links, site)
    # ---
    if not editors:
        printe.output('<<red>> no editors')
        return
    # ---
    if 'dump' in sys.argv:
        print('json.dumps(editors, indent=4)')
        return
    # ---
    title = f"WikiProjectMed:WikiProject_Medicine/Stats/Top_medical_editors_2023/{site}"
    # ---
    text = '{{:WPM:WikiProject Medicine/Total medical articles}}\n'
    text += '{{Top medical editors 2023 by lang}}\n'
    # ---
    if site != 'ar':
        text += f'Numbers of 2023. There are {len(links):,} articles in {site}\n'
    # ---
    text += '''{| class="sortable wikitable"\n!#\n!User\n!Count\n|-'''
    # ---
    for i, (user, count) in enumerate(editors.items(), start=1):
        # ---
        user = user.replace('_', ' ')
        # ---
        text += f'\n|-\n!{i}\n|[[:w:{site}:{user}|{user}]]\n|{count:,}'
        # ---
    # ---
    text += '\n|}'
    # ---
    page = md_MainPage(title, 'www', family='mdwiki')
    page.save(newtext=text, summary='update', nocreate=0, minor='')
    # ---
    return editors

def start():
    # ---
    p_site = ''
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        if arg == 'site':
            p_site = value
    # ---
    # read json files in sites_dir
    files = os.listdir(sites_dir)
    # sort
    files.sort()
    # ---
    for numb, file in enumerate(files, start=1):
        # ---
        printe.output(f'<<lightgreen>> n: {numb} file: {file}:')
        # ---
        if not file.endswith('wiki.json'):
            continue
        # ---
        site = file[:-5]
        # ---
        if p_site and f'{p_site}wiki' != site:
            continue
        # ---
        with open(sites_dir / file, 'r', encoding='utf-8') as f:
            links = json.load(f)
        # ---
        work_in_one_site(site, links)

if __name__ == "__main__":
    start()
