'''

'''
# ---
import os
import json
import sys
from pathlib import Path
# ---
from mdpy import printe
from mdpy.bots import wikidataapi
from stats.qids import qids_list
# ---
Dir = Path(__file__).parent

# make dir sites
if not os.path.exists(Dir / 'sites'):
    os.mkdir(Dir / 'sites')

def get_sitelinks(qs_list, lena=300):
    # ---
    qs_list = list(qs_list)
    # ---
    params_wd = {
        "action": "wbgetentities",
        "format": "json",
        # "ids": ,
        "redirects": "yes",
        "props": "sitelinks",
        "utf8": 1,
    }
    # ---
    all_entities = {}
    # ---
    for i in range(0, len(qs_list), lena):
        # ---
        qids = qs_list[i : i + lena]
        # ---
        params_wd["ids"] = '|'.join(qids)
        # ---
        printe.output(f'<<lightgreen>> done:{len(all_entities)} from {len(qs_list)}, get sitelinks for {len(qids)} qids.')
        # ---
        json1 = wikidataapi.post(params_wd, apiurl='https://www.wikidata.org/w/api.php')
        # ---
        if json1:
            # ---
            entities = json1.get("entities", {})
            # ---
            all_entities = {**all_entities, **entities}
    # ---
    sitelinks = {}
    # ---
    for _qid_1, kk in all_entities.items():
        # ---
        # "abwiki": {"site": "abwiki","title": "Обама, Барак","badges": []}
        # ---
        for _, tab in kk.get("sitelinks", {}).items():
            # ---
            title = tab.get("title", '')
            site  = tab.get("site", '')
            # ---
            if not site in sitelinks:
                sitelinks[site] = []
            # ---
            sitelinks[site].append(title)
    # ---
    return sitelinks

def start():
    # ---
    sits = get_sitelinks(qids_list, lena=500)
    # ---
    # dump each site to file
    for site, links in sits.items():
        # ---
        with open(Dir / 'sites' / f'{site}.json', 'w', encoding='utf-8') as f:
            json.dump(links, f, sort_keys=True)
            printe.output(f'dump <<lightgreen>> {site} of {len(links)}')

if __name__ == "__main__":
    start()
