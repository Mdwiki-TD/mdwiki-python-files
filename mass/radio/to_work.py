'''

python3 core8/pwb.py mass/radio/to_work

from mass.radio.to_work import ids_to_work
'''
from mass.radio.jsons_files import jsons, dumps_jsons, ids_to_urls, urls_to_ids
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, ids=0, all_ids=0, urls_to_get_info=0)
# ---
print(f"lenth of jsons.urls: {len(jsons.urls)}")
# ---
casesin_to_urls = [ids_to_urls.get(str(ca_id)) for ca_id in jsons.cases_in_ids.keys() if ids_to_urls.get(str(ca_id))]
# ---
print(f"lenth of jsons.cases_in: {len(jsons.cases_in_ids)}, lenth of casesin_to_urls: {len(casesin_to_urls)}")
# ---
t_to_work = [url for url in jsons.urls.keys() if url not in casesin_to_urls]
# ---
ids_to_work = {
    urls_to_ids.get(url): jsons.ids.get(urls_to_ids.get(url))
    for url in t_to_work
    if urls_to_ids.get(url) and jsons.ids.get(urls_to_ids.get(url))
}
# ---
print(f"lenth of t_to_work: {len(t_to_work)}")
print(f"lenth of ids_to_work: {len(ids_to_work)}")
# ---
rm2 = {x: v for x, v in ids_to_work.items() if jsons.cases_in_ids.get(x)}
# ---
print(f"lenth of rm2: {len(rm2)}")
# ---
if __name__ == '__main__':
    # items in jsons.urls and not in jsons.cases_in_ids
    jsons.to_work = t_to_work

    # dump jsons.to_work to to_work.json
    dumps_jsons(to_work=1)
