'''
python pwb.py niosh/bot
python3 core8/pwb.py niosh/bot
'''
import sys
import os
from pathlib import Path
import re
import json

# ---
from newapi.wiki_page import MainPage, NEW_API

# ---
Dir = Path(__file__).parent
Dir2 = os.path.dirname(Dir)
# ---
file_json1 = f"{Dir}/jsons/extlinks.json"
# ---
if not os.path.isfile(file_json1):
    with open(file_json1, "w", encoding="utf-8") as aa:
        json.dump({}, aa)

totox = {}
# ---
with open(file_json1, "r", encoding="utf-8") as f:
    totox = json.load(f)
# ---
file_json2 = f"{Dir}/jsons/niosh.json"
file_all_links = f"{Dir}/jsons/all_links.json"
# ---
if not os.path.isfile(file_json2):
    with open(file_json2, "w", encoding="utf-8") as aa:
        json.dump({}, aa)

with open(file_json2, "r", encoding="utf-8") as cc:
    new = json.load(cc)


def new_search():
    global totox
    totox = {}
    # ---
    api_new = NEW_API('en', family='wikipedia')
    # ---
    vv = 'insource:"cdc.gov/niosh/"'
    search = api_new.Search(value=vv, ns="0", offset='', srlimit="", RETURN_dict=False, addparams={})
    # ---
    na = 0
    nn = len(search)
    # ---
    for x in search:
        na += 1
        page = MainPage(x, 'en', family='wikipedia')
        print(f'p:{na}/{nn}, title:{x}, get_extlinks:')
        extlinks = page.get_extlinks()
        totox[x] = extlinks
    # ---
    with open(file_json1, "w", encoding="utf-8") as dd:
        json.dump(totox, dd)


def new_vals():
    # ---
    global new
    new = {}

    def fix_links(x):
        # remove url suffix like https://web.archive.org/web/20150530203735/

        x = re.sub(r'^https?://web\.archive\.org/web/\d+/(.*)', r'\1', x.strip())

        x = x.split("#")[0].strip()
        x = re.sub(r'^https*://(www.|)cdc.gov/', 'https://www.cdc.gov/', x)
        return x

    # ---
    for title, exts in totox.items():
        tat = []
        # ---
        for x in exts:
            if x.find('cdc.gov/niosh/') == -1:
                continue
            # ---
            if x.find('web.archive.org') > -1:
                x = fix_links(x)
            # ---
            tat.append(x)
        # ---
        if tat:
            new[title] = tat
    # ---
    new = {k: v for k, v in sorted(new.items(), key=lambda item: item[0].lower(), reverse=False)}
    # ---
    with open(file_json2, "w", encoding="utf-8") as ee:
        json.dump(new, ee, ensure_ascii=False, indent=2)


def start():
    # ---
    if 'new' in sys.argv:
        new_search()
    # ---
    if 'new2' in sys.argv:
        new_vals()
    # ---
    n = 0
    # ---
    all_links = []
    # ---
    for _x, exts in new.items():
        n += 1
        all_links.extend(exts)
        # print(f'n:{n}/{len(new.keys())}, title:{x} length:{len(exts)}')
    # ---
    all_links = sorted(set(all_links))
    # ---
    # ---
    with open(file_all_links, "w", encoding="utf-8") as ff:
        json.dump(all_links, ff, ensure_ascii=False, indent=2)
    # ---
    len_all_links = len(all_links)
    # ---
    print(f'all pages:{n}, {len_all_links=}')


if __name__ == "__main__":
    start()
