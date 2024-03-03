# mass/radio/all_cats_utils.py
from mass.radio.jsons_files import dumps_jsons, ids_to_urls, jsons, urls_to_ids
from newapi.ncc_page import MainPage as ncc_MainPage


def generate_text():
    text = '* Radiopaedia cases by category\n'
    text += f'* All Cases: {len(jsons.all_ids)}\n'
    text += '{| class="wikitable sortable"\n|-\n'
    text += '!#!!Category\n|-\n'
    n = 0

    for _, tab in jsons.all_ids.items():
        caseId = tab['caseId']
        title = tab['title']
        category = f'Radiopaedia case {caseId} {title}'
        n += 1
        text += f'!{n}||[[:Category:{category}]]\n'
        text += '|-\n'

    text += '|}'
    text += '\n[[Category:Radiopaedia|*]]'
    return text

def save_page(text):
    page = ncc_MainPage('User:Mr._Ibrahem/Radiopaedia', 'www', family='nccommons')
    page.save(newtext=text, summary='update', nocreate=0, minor='')

def extract_utility_functions():
    text = generate_text()
    save_page(text)

if __name__ == "__main__":
    extract_utility_functions()
