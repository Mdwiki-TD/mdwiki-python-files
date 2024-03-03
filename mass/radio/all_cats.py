# -*- coding: utf-8 -*-
"""
python3 core8/pwb.py mass/radio/all_cats ask

"""
from newapi.ncc_page import MainPage as ncc_MainPage
from mass.radio.jsons_files import jsons, dumps_jsons, ids_to_urls, urls_to_ids
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, all_ids=0, urls_to_get_info=0)
# ---

def doo():
    text = '* Radiopaedia cases by category\n'
    # ---
    text += f'* All Cases: {len(jsons.all_ids)}\n'
    print(text)
    # ---
    text += '{| class="wikitable sortable"\n|-\n'
    text += '!#!!Category'
    # text += '!! Image set'
    text += '\n|-\n'
    n = 0

    for _, tab in jsons.all_ids.items():
        caseId = tab['caseId']
        title = tab['title']
        category = f'Radiopaedia case {caseId} {title}'
        n += 1
        text += f'!{n}||[[:Category:{category}]]\n'
        # text += f'| [[{category}]]\n'
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
