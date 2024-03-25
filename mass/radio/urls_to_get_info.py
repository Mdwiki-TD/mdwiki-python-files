"""

python3 core8/pwb.py mass/radio/urls_to_get_info

"""

import os

import psutil

from mass.radio.jsons_files import (dump_json_file, ids_to_urls, jsons,
                                    urls_to_ids)

# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, all_ids=0, urls_to_get_info=0)

# Step 1: Calculate the difference between jsons.urls and urls_to_ids
urls_to_get_info = set(jsons.urls.keys()) - set(urls_to_ids.keys())
mins = len(jsons.urls) - len(urls_to_get_info)

print(f"Length of jsons.urls: {len(jsons.urls)}")
print(f"Length of urls_to_get_info: {len(urls_to_get_info)}, mins: {mins}")

# Step 2: Filter casesin_to_urls using list comprehension
casesin_to_urls = [
    ids_to_urls.get(str(ca_id)) for ca_id in jsons.cases_in_ids.keys()
    if str(ca_id) in ids_to_urls
]

print(
    f"Length of jsons.cases_in_ids: {len(jsons.cases_in_ids)}, Length of casesin_to_urls: {len(casesin_to_urls)}"
)

# Step 3: Remove duplicates efficiently using set intersection
already_done_urls = set(casesin_to_urls) & urls_to_get_info
already_done = len(already_done_urls)
urls_to_get_info -= already_done_urls

print(
    f"Already done: {already_done}, Length of urls_to_get_info: {len(urls_to_get_info)}"
)

# Step 4: Save the dictionary to a JSON file
dump_json_file("jsons/urls_to_get_info.json", list(urls_to_get_info), False)
# dumps_jsons(urls_to_get_info=1)

print("Step 5: Saved urls_to_get_info dictionary to jsons.")

usage = psutil.Process(os.getpid()).memory_info().rss
print(f"memory usage: psutil {usage / 1024 / 1024} MB")
# memory usage: psutil 253.40234375 MB
