'''

python3 core8/pwb.py mass/radio/authors_list/auths_cats break

tfj run aucts --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/authors_list/auths_cats"

logs in page:
https://nccommons.org/wiki/User:Mr._Ibrahem/Radiopaedia_authors

from mass.radio.authors_list import auths_cats
# auth_cats = auths_cats.get_auth_cats(id2cat, auth)

'''
import re
import sys
import json
import os
from pathlib import Path
from multiprocessing import Pool
from newapi import printe
from newapi.ncc_page import CatDepth
from newapi.ncc_page import MainPage as ncc_MainPage
from mass.radio.lists.cases_to_cats import cases_cats  # cases_cats()
# ---
main_dir = Path(__file__).parent.parent
# ---
with open(main_dir / 'authors_list' / 'authors_to_cases.json', 'r', encoding='utf-8') as f:
    authors_to_cases = json.load(f)
# ---
with open(os.path.join(str(main_dir), 'authors_list/authors_infos.json'), 'r', encoding='utf-8') as f:
    authors_infos = json.load(f)
# ---
print(f"Length of authors_to_cases: {len(authors_to_cases)}")
# ---


def create_cat(cat, text):
    page = ncc_MainPage(cat, 'www', family='nccommons')

    if page.exists():
        pa_text = page.get_text()
        if pa_text == text:
            print("no different")
            return
        page.save(newtext=text, summary='create')
    else:
        page.Create(text=text, summary='create')


def add(da=[], title="", cat=""):
    if da:
        title, cat = da[0], da[1]
    # ---
    page = ncc_MainPage(title, 'www', family='nccommons')

    if not page.exists():
        return

    text = page.get_text()
    # ---
    if text.find(cat) != -1:
        printe.output(f"cat {title} already has it.")
        return
    # ---
    newtext = text
    newtext += f"\n[[{cat}]]"
    # ---
    page.save(newtext=newtext, summary=f'Bot: added [[:{cat}]]')


def mu(tab):
    pool = Pool(processes=3)
    pool.map(add, tab)
    pool.close()
    pool.terminate()


def add_cat(pages, cat):
    if "multi" in sys.argv:
        tab = [[x, cat] for x in pages]
        mu(tab)
    else:
        for title in pages:
            add(title=title, cat=cat)


def one_auth(auth, cat_list):
    printe.output(f"Author: {auth}, {len(cat_list)=}")
    # ---
    cat = f"Category:Radiopaedia cases by {auth}"
    text = ""
    # ---
    url = authors_infos.get(auth, {}).get('url')
    location = authors_infos.get(auth, {}).get('location')
    # ---
    if url:
        text += f"* Author: [{url} {auth}]\n"
    else:
        text += f"* Author: {auth}\n"
    # ---
    text += f"[[Category:Radiopaedia cases by author|{auth}]]"
    # ---
    create_cat(cat, text)
    # ---
    done = CatDepth(cat, sitecode='www', family="nccommons", depth=0, ns="14")
    # ---
    new_cat_list = [x for x in cat_list if x not in done]
    # ---
    printe.output(f"{len(done)=}, {len(new_cat_list)=}")
    # ---
    if "noadd" not in sys.argv:
        add_cat(new_cat_list, cat)


def get_auth_cats(cats, auth):
    cat_list = [cats[c] for c in authors_to_cases.get(auth, []) if c in cats]
    # ---
    printe.output(f"get_auth_cats: {auth=}, {len(cat_list)=}")
    # ---
    return cat_list


def start():
    # ---
    cats = cases_cats()
    # ---
    # auths in authors_to_cases with > 10 cases
    authors_cases = {k: v for k, v in authors_to_cases.items() if len(v) > 1}
    # ---
    for numb, (x, x_cases) in enumerate(authors_cases.items(), start=1):
        # ---
        printe.output(f"{x=}, cases: {len(x_cases)=}")
        # ---
        cat_list = [cats[c] for c in x_cases if c in cats]
        cat_no_list = [c for c in x_cases if c not in cats]
        # ---
        printe.output(f"<<red>> {len(cat_no_list)=}")
        # ---
        one_auth(x, cat_list)
        # ---
        if "break" in sys.argv and numb % 10 == 0:
            break


if __name__ == '__main__':
    start()
