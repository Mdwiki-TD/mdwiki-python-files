'''

python3 core8/pwb.py mass/radio/to_work

from mass.radio.to_work import ids_to_work
'''
from mass.radio.jsons_files import jsons, dumps_jsons, ids_to_urls, urls_to_ids, dump_json_file
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, ids=0, all_ids=0, urls_to_get_info=0)

cases_in_ids = set(jsons.cases_in_ids.keys())
urls_set = set(jsons.urls.keys())

casesin_to_urls = [ids_to_urls.get(str(ca_id)) for ca_id in cases_in_ids if ids_to_urls.get(str(ca_id))]

t_to_work = urls_set - set(casesin_to_urls)

ids_to_work = {
    urls_to_ids.get(url): jsons.ids.get(urls_to_ids.get(url))
    for url in t_to_work
    if urls_to_ids.get(url) and jsons.ids.get(urls_to_ids.get(url))
}

rm2 = {x: v for x, v in ids_to_work.items() if x in cases_in_ids}

print(f"Length of jsons.urls: {len(urls_set)}")
print(f"Length of jsons.cases_in: {len(cases_in_ids)}, Length of casesin_to_urls: {len(casesin_to_urls)}")
print(f"Length of t_to_work: {len(t_to_work)}")
print(f"Length of ids_to_work: {len(ids_to_work)}")
print(f"Length of rm2: {len(rm2)}")

del rm2
del casesin_to_urls

if __name__ == '__main__':
    # items in jsons.urls and not in jsons.cases_in_ids
    # jsons._replace(to_work = list(t_to_work))

    # dump jsons.to_work to to_work.json
    # dumps_jsons(to_work=1)
    dump_json_file('jsons/to_work.json', list(t_to_work), False)

else:
    del t_to_work
