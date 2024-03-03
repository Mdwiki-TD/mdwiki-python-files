'''

python3 core8/pwb.py mass/radio/authors_list/bot nodump
python3 core8/pwb.py mass/radio/authors_list/bot

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
with open(os.path.join(str(main_dir), 'jsons/infos.json'), 'r', encoding='utf-8') as f:
    infos = json.load(f)
# ---
with open(os.path.join(str(main_dir), 'jsons/authors.json'), 'r', encoding='utf-8') as f:
    authors = json.load(f)
# ---
with open(os.path.join(str(main_dir), 'jsons/all_ids.json'), 'r', encoding='utf-8') as f:
    all_ids = json.load(f)
# ---
print(f"Length of all_ids: {len(all_ids)}")
# ---
def get_missing_authors():
    printe.output("<<yellow>> get_missing_authors:")
    # ---
    updated_authors = authors.copy()
    # ---
    add = 0
    add_from_info = 0
    # ---
    for x, ta in all_ids.items():
        author_exists = authors.get(x)
        # ---
        if author_exists:
            continue
        # ---
        url = ta.get('url', None)
        # ---
        if not x or x in updated_authors:
            continue
        # ---
        author = ta.get('author', "")
        # ---
        if not author:
            author = infos.get(url, {}).get('author', "")
            if author:
                add_from_info += 1
        # ---
        updated_authors[x] = author
        # ---
        add += 1
    # ---
    print(f"Added from all_ids: {add:,}")
    print(f"add_from_info: {add_from_info:,}")
    # ---
    # sort updated_authors by int(k)
    updated_authors = dict(sorted(updated_authors.items(), key=lambda x: int(x[0])))
    # ---
    if "nodump" not in sys.argv:
        # with open(os.path.join(str(main_dir), 'authors_list/authors_new.json'), 'w', encoding='utf-8') as f:
        with open(os.path.join(str(main_dir), 'jsons/authors.json'), 'w', encoding='utf-8') as f:
            json.dump(updated_authors, f, ensure_ascii=False, indent=4)
    # ---
    # len of empty authors
    print("empty authors:", len([x for x, v in updated_authors.items() if not v]))
    # ---
    return updated_authors

def make_authors_list(authors_n):
    printe.output("<<yellow>> make_authors_list:")
    # ---
    # list of authors by length
    new_authors = {}
    # ---
    for x, v in authors_n.items():
        if not v:
            continue
        # ---
        new_authors.setdefault(v, []).append(x)
    # ---
    print("len new_authors:", len(new_authors))
    # ---
    # sort
    new_authors = dict(sorted(new_authors.items(), key=lambda x: len(x[1]), reverse=True))
    # ---
    printe.output("<<yellow>> new_authors:")
    # ---
    for num, (x, v) in enumerate(new_authors.items(), 1):
        print(f"author({num}/{len(new_authors)}): {x}: cases: {len(v)}")
        if num > 10:
            break
    # ---
    if "nodump" not in sys.argv:
        with open(os.path.join(str(main_dir), 'authors_list/authors_to_cases.json'), 'w', encoding='utf-8') as f:
            json.dump(new_authors, f, ensure_ascii=False, indent=4)
    # ---
    # print sum of all new_authors values
    print("sum of all new_authors values:", sum([len(x) for x in new_authors.values()]))
    # ---
    return new_authors

def make_authors_infos(auths):
    # ---
    auths_infos = {x: {} for x in auths.keys()}
    # ---
    for x in auths.keys():
        first_case = auths[x][0]
        first_case_url = all_ids.get(first_case, {}).get('url', None)
        auths_infos[x] = get_author_infos(x, first_case_url)
        # ---
        if "break" in sys.argv:
            break
    # ---
    if "nodump" not in sys.argv:
        with open(os.path.join(str(main_dir), 'authors_list/authors_infos.json'), 'w', encoding='utf-8') as f:
            json.dump(auths_infos, f, ensure_ascii=False, indent=4)
    # ---
def start():
    authors_n = get_missing_authors()

    new = make_authors_list(authors_n)

    make_authors_infos(new)
    

if __name__ == '__main__':
    start()