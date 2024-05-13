"""
from mass.eyerounds.bots.catbot import category_name

python3 core8/pwb.py mass/eyerounds/bots/catbot

"""
import re
import json
from pathlib import Path

from mass.eyerounds.bots.url_to_title import urls_to_title

# Specify the root folder
main_dir = Path(__file__).parent.parent

with open(main_dir / 'jsons/urls.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def category_name(url):
    # url: https://eyerounds.org/cases/141-Myeloid-Sarcoma.htm
    # EyeRounds Case
    cat = ''
    # ---
    title = urls_to_title.get(url, '')
    # match title and number from url
    ma = re.search(r'/(\d+)[_-](.*)\.htm', url)
    # https://eyerounds.org/cases/case28.htm
    ma2 = re.search(r'/(case\d+)\.htm', url)
    numb = 0
    if ma:
        numb = ma.group(1)
        cat = f'EyeRounds Case {ma.group(1)} {ma.group(2)}'
    elif title and ma2:
        numb = ma2.group(1)
        cat = f'EyeRounds {ma2.group(1)} {title}'
    # ---
    cat = cat.replace("-", " ")
    cat = cat.replace(":", "")
    # ---
    return cat, numb

def so():
    cats = {}
    no_cat = 0
    for _, info_data in data.items():
        for x in info_data.get("cases", {}):
            url = x['url']
            cat, numb = category_name(url)
            cats[url] = cat
            if not cat:
                no_cat += 1
                print(f'{url} -> {cat}')
    with open(main_dir / 'jsons/urls_to_cat.json', 'w', encoding='utf-8') as f:
        json.dump(cats, f, indent=2)

    print(f"{no_cat} urls have no category")

if __name__ == '__main__':
    so()
