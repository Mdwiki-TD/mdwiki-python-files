'''

# ---
python3 core8/pwb.py mass/radio/jsons_files

from mass.radio.jsons_files import jsons, dumps_jsons, ids_to_urls, urls_to_ids
#  jsons.urls
#  jsons.infos
#  jsons.cases_in_ids
#  jsons.cases_dup
#  jsons.to_work
#  jsons.ids
#  jsons.all_ids
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, ids=0, all_ids=0, urls_to_get_info=0, systems=0, url_to_sys=0)
# ---
'''
import sys
import os
from pathlib import Path
import json
from collections import namedtuple
from new_api import printe
main_dir = Path(__file__).parent

files = {
    "url_to_sys": os.path.join(str(main_dir), 'jsons/url_to_sys.json'),
    "authors": os.path.join(str(main_dir), 'jsons/authors.json'),
    "cases_dup": os.path.join(str(main_dir), 'jsons/cases_dup.json'),
    "cases_in_ids": os.path.join(str(main_dir), 'jsons/cases_in_ids.json'),
    "ids": os.path.join(str(main_dir), 'jsons/ids.json'),
    "all_ids": os.path.join(str(main_dir), 'jsons/all_ids.json'),
    "infos": os.path.join(str(main_dir), 'jsons/infos.json'),
    "to_work": os.path.join(str(main_dir), 'jsons/to_work.json'),
    "urls": os.path.join(str(main_dir), 'jsons/urls.json'),
    "urls_to_get_info": os.path.join(str(main_dir), 'jsons/urls_to_get_info.json'),
    "systems": os.path.join(str(main_dir), 'jsons/systems.json'),
}

jsons = namedtuple('jsons', files.keys())
datas = {}
for k, v in files.items():
    if not os.path.exists(v):
        with open(v, 'w', encoding='utf-8') as f:
            f.write("{}")
    with open(v, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
        datas[k] = data
# ---
jsons.url_to_sys = datas['url_to_sys']
jsons.authors = datas['authors']
jsons.cases_dup = datas['cases_dup']
jsons.cases_in_ids = datas['cases_in_ids']
jsons.ids = datas['ids']
jsons.all_ids = datas['all_ids']
jsons.infos = datas['infos']
jsons.to_work = datas['to_work']
jsons.urls = datas['urls']
jsons.urls_to_get_info = datas['urls_to_get_info']
jsons.systems = datas['systems']
# ---
ids_to_urls = {str(v['caseId']): v['url'] for k, v in jsons.all_ids.items()}
urls_to_ids = {v['url']: str(v['caseId']) for k, v in jsons.all_ids.items()}
# ---


def dumps_jsons(**kwargs):
    def du(file, data):
        printe.output(f'<<lightyellow>> dumps_jsons: {file}')
        # ---
        if not data:
            printe.output('<<red>> data is empty')
            return
        # ---
        if 'nodump' in sys.argv:
            return
        # ---
        if kwargs.get('sort'):
            data = dict(sorted(data.items()))
        # ---
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    # ---
    # alert if key not in files
    for k in kwargs.keys():
        if k not in files.keys():
            printe.output(f'<<red>> key {k} not in files')
    # ---
    if kwargs.get('url_to_sys'):
        du(files['url_to_sys'], jsons.url_to_sys)
    if kwargs.get('authors'):
        du(files['authors'], jsons.authors)
    # ---
    if kwargs.get('cases_dup'):
        du(files['cases_dup'], jsons.cases_dup)
    # ---
    if kwargs.get('cases_in_ids'):
        du(files['cases_in_ids'], jsons.cases_in_ids)
    # ---
    if kwargs.get('ids'):
        du(files['ids'], jsons.ids)
    # ---
    if kwargs.get('all_ids'):
        du(files['all_ids'], jsons.all_ids)
    # ---
    if kwargs.get('infos'):
        du(files['infos'], jsons.infos)
    # ---
    if kwargs.get('to_work'):
        du(files['to_work'], jsons.to_work)
    # ---
    if kwargs.get('urls'):
        du(files['urls'], jsons.urls)
    # ---
    if kwargs.get('urls_to_get_info'):
        du(files['urls_to_get_info'], jsons.urls_to_get_info)
    # ---
    if kwargs.get('systems'):
        du(files['systems'], jsons.systems)
    # ---


if __name__ == "__main__":
    # print lenth of all jsons
    for n, (k, v) in enumerate(datas.items(), start=1):
        print(f"file: {k.ljust(20)} len: {len(v):,}")

    print(f"file: urls_to_ids     len: {len(urls_to_ids):,}")
    print(f"file: ids_to_urls     len: {len(ids_to_urls):,}")
