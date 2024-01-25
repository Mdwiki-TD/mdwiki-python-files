'''

python3 core8/pwb.py mass/radio/start nodiff test
python3 core8/pwb.py mass/radio/start nodiff get:55

'''
import re
import sys
from new_api import printe
from new_api.ncc_page import CatDepth
from mass.radio.One_Case import OneCase
from mass.radio.to_work import ids_to_work
from mass.radio.jsons_files import jsons, dumps_jsons, ids_to_urls, urls_to_ids
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, ids=0, all_ids=0, urls_to_get_info=0)

pages_all = {}
cases_in_ids = []
def get_pages():
    printe.output('<<purple>> start.py get_pages:')
    pages = CatDepth('Category:Uploads by Mr. Ibrahem', sitecode='www', family="nccommons", depth=0, ns="all")
    pages3 = CatDepth('Category:Radiopaedia sets', sitecode='www', family="nccommons", depth=0, ns="all")

    pages2 = CatDepth('Category:Radiopaedia images by case', sitecode='www', family="nccommons", depth=0, ns="all")

    pages = pages | pages2
    pages = pages | pages3
    # ---
    reg = r'^Category:Radiopaedia case (\d+) (.*?)$'
    # ---
    for cat in pages2:
        match = re.match(reg, cat)
        if match:
            cases_in_ids.append(str(match.group(1)))
    # ---
    return pages

def main(ids_tab):
    global pages_all
    printe.output(f'<<purple>> start.py all: {len(ids_tab)}:')

    if 'test' not in sys.argv:
        tabs = {}
        print(f'all cases: {len(ids_tab)}')
        length = len(ids_tab) // 13
        for i in range(0, len(ids_tab), length):
            num = i//length+1
            tabs[str(num)] = dict(list(ids_tab.items())[i : i + length])
            # print(f'tab {num} : {len(tabs[str(num)])}')
            print(f'tfj run sta{num} --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:{num} {len(tabs[str(num)])}"')

        for arg in sys.argv:
            arg, _, value = arg.partition(':')
            if arg == 'get':
                ids_tab = tabs[value]
                print(f'work in {len(ids_tab)} cases')

    if pages_all == {}:
        pages_all = get_pages()

    printe.output(f'<<purple>> pages_all: {len(pages_all)}:')
    printe.output(f'<<purple>> cases_in_ids: {len(cases_in_ids)}:')

    n = 0
    for k, tab in ids_tab.items():
        n += 1
        # ---
        caseId   = tab['caseId']
        case_url = tab['url']
        # ---
        printe.output('++++++++++++++++++++++++++++++++')
        printe.output(f'<<purple>> case:{n} / {len(ids_tab)}, caseId:{caseId}')
        # ---
        if caseId in jsons.cases_in_ids:
            printe.output(f'<<purple>> caseId {caseId} already in jsons.cases_in_ids')
            continue
        # ---
        if str(caseId) in cases_in_ids:
            printe.output(f'<<purple>> caseId {caseId} already in cases_in_ids')
            continue
        # ---
        author = tab.get('author', '')
        # ---
        if not author:
            author = jsons.infos.get(case_url, {}).get(str(caseId), '')
        # ---
        if not author:
            author = jsons.authors.get(str(caseId), '')
        # ---
        title = tab['title']
        # ---
        studies = [study.split('/')[-1] for study in tab['studies']]
        # ---
        bot = OneCase(case_url, caseId, title, studies, pages_all, author)
        bot.start()
        # ---
        if n % 100 == 0:
            print(f'processed {n} cases')

if __name__ == "__main__":
    ids_by_caseId = jsons.ids
    # ---
    print('ids_by_caseId: ', len(ids_by_caseId))
    print('jsons.to_work: ', len(jsons.to_work))
    print('ids_to_work: ', len(ids_to_work))
    # ---
    if 'test' in sys.argv:
        ids_by_caseId = {
            "20476": {
                "url": "https://radiopaedia.org/cases/peritonsillar-abscess-quinsy",
                "caseId": 20476,
                "title": "Peritonsillar abscess (quinsy)",
                "studies": [
                    "https://radiopaedia.org/cases/20476/studies/20387"
                ],
                "author": "Chris O'Donnell"
            }
        }
    # ---
    main(ids_by_caseId)
