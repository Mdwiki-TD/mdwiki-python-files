'''

python3 core8/pwb.py mass/radio/urls_to_get_info

'''
# ---
from mass.radio.jsons_files import jsons, dumps_jsons, ids_to_urls, urls_to_ids
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, ids=0, all_ids=0, urls_to_get_info=0)

print(f"lenth of jsons.urls: {len(jsons.urls)}")
# ---
urls_to_get_info = [ url for url in jsons.urls.keys() if url not in urls_to_ids.keys() ]
# ---
mins = len(jsons.urls) - len(urls_to_get_info)
# ---
print(f"lenth of urls_to_get_info: {len(urls_to_get_info)}, mins: {mins}")
# ---
casesin_to_urls = [ ids_to_urls.get(str(ca_id)) for ca_id in jsons.cases_in_ids.keys() if ids_to_urls.get(str(ca_id)) ]
print(f"lenth of jsons.cases_in_ids: {len(jsons.cases_in_ids)}, lenth of casesin_to_urls: {len(casesin_to_urls)}")
# ---
already_done = 0
# ---
for url2 in casesin_to_urls:
    if url2 in urls_to_get_info:
        urls_to_get_info.remove(url2)
        already_done += 1
# ---
print(f"already_done: {already_done}, urls_to_get_info: {len(urls_to_get_info)}")
# ---
print("Step 5: Saved urls_to_get_info dictionary to jsons.")

jsons.urls_to_get_info = urls_to_get_info

# Step 5: Save the dictionary to a JSON file
dumps_jsons(urls_to_get_info=1)
