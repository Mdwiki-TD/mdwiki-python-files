'''
python3 core8/pwb.py mass/radio/jsons_files

from mass.radio.jsons_files import jsons, dumps_jsons, ids_to_urls, urls_to_ids
#  jsons.urls
#  jsons.infos
#  jsons.cases_in_ids
#  jsons.cases_dup
#  jsons.to_work
#  jsons.all_ids
#  jsons.cases_cats
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, all_ids=0, urls_to_get_info=0, systems=0, url_to_sys=0)

'''
import psutil
import sys
import os
import json
from collections import namedtuple
from pathlib import Path
from newapi import printe

main_dir = Path(__file__).parent


def load_json_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("{}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.loads(f.read())


def dump_json_file(file_path, data, Sort):
    printe.output(f'<<lightyellow>> dumps_jsons: {file_path}')
    if not data:
        printe.output('<<red>> data is empty')
        return
    if 'nodump' in sys.argv:
        return

    if Sort:
        data = dict(sorted(data.items()))

    with open(main_dir / file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


files = {
    "url_to_sys": 'jsons/url_to_sys.json',
    "authors": 'jsons/authors.json',
    "cases_dup": 'jsons/cases_dup.json',
    "cases_in_ids": 'jsons/cases_in_ids.json',
    "ids": 'jsons/ids.json',
    "cases_cats": 'jsons/cases_cats.json',
    "all_ids": 'jsons/all_ids.json',
    "infos": 'jsons/infos.json',
    "to_work": 'jsons/to_work.json',
    "urls": 'jsons/urls.json',
    "urls_to_get_info": 'jsons/urls_to_get_info.json',
    "systems": 'jsons/systems.json',
}

jsons = namedtuple('jsons', files.keys())
datas = {k: load_json_file(main_dir / v) for k, v in files.items()}

jsons = jsons(**{key: value.copy() for key, value in datas.items()})

ids_to_urls = {str(v['caseId']): v['url'] for k, v in jsons.all_ids.items()}
urls_to_ids = {v['url']: str(v['caseId']) for k, v in jsons.all_ids.items()}


def dumps_jsons(**kwargs):
    # ---
    Sort = kwargs.get('sort')
    # ---
    for key in kwargs.keys():
        file_path = files.get(key)
        if file_path:
            value = getattr(jsons, key)
            dump_json_file(main_dir / file_path, value, Sort)
        else:
            printe.output(f'<<red>> key {key} not in files')


if __name__ == "__main__":
    # print length of all jsons
    for n, (k, v) in enumerate(datas.items(), start=1):
        print(f"{n}, file: {k.ljust(20)} len: {len(v):,}")

    print(f"file: urls_to_ids     len: {len(urls_to_ids):,}")
    print(f"file: ids_to_urls     len: {len(ids_to_urls):,}")

    usage = psutil.Process(os.getpid()).memory_info().rss
    printe.output(f'<<red>> memory usage: psutil {usage / 1024 / 1024} MB')
else:
    del datas
