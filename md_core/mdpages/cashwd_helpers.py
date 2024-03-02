import json
import os
import traceback
from datetime import datetime
from pathlib import Path

from mdpy import printe
from mdpy.bots import en_to_md, mdwiki_api, sql_for_mdwiki, wikidataapi
from mdpy.bots.check_title import valid_title


def get_qids_sitelinks(qidslist):
    # Implementation of the get_qids_sitelinks function

def extract_titles_from_categories():
    # Implementation of the extract_titles_from_categories function

def dump_sitelinks_to_json(lists):
    # Implementation of the dump_sitelinks_to_json function

def dump_missing_to_json(missing):
    # Implementation of the dump_missing_to_json function

def dump_exists_to_json(main_table_sites):
    # Implementation of the dump_exists_to_json function

def dump_noqids_to_json(noqids):
    # Implementation of the dump_noqids_to_json function

def print_redirects_qids(redirects_qids):
    # Implementation of the print_redirects_qids function

def print_missing_qids(mis_qids):
    # Implementation of the print_missing_qids function

def cash_wd():
    # Implementation of the cash_wd function
    titles = extract_titles_from_categories()
    printe.output(f'<<lightgreen>> len of mdwiki_api.subcatquery:RTT:{len(titles)}.')
    qids_list = {}
    missing['all'] = len(titles)
    for x in titles:
        qid = en_to_md.mdtitle_to_qid.get(x, '')
        if qid != '':
            qids_list[qid] = x
    lists, _table_l = get_qids_sitelinks(qids_list)
    dump_sitelinks_to_json(lists)
    for site, miss_list in main_table_sites.items():
        miss_list = list(set(miss_list))
        leeen = len(titles) - len(miss_list)
        missing['langs'][site] = {'missing': leeen, 'exists': len(miss_list)}
        json_file = f'{Dashboard_path}/cash_exists/{site}.json'
        if not os.path.exists(json_file):
            printe.output(f'.... <<lightred>> file:"{site}.json not exists ....')
        try:
            with open(json_file, 'w', encoding="utf-8") as aa:
                json.dump(miss_list, aa, ensure_ascii=False, indent=4)
            printe.output(f'<<lightgreenn>>dump to cash_exists/{site}.json done..')
        except Exception:
            pywikibot.output('Traceback (most recent call last):')
            pywikibot.output(traceback.format_exc())
            pywikibot.output('CRITICAL:')
            continue
    noqids = sorted([x for x in titles if x not in en_to_md.mdtitle_to_qid])
    with open(f'{Dashboard_path}/Tables/noqids.json', 'w', encoding="utf-8") as dd:
        json.dump(noqids, dd)
    for old_q, new_q in redirects_qids.items():
        print_redirects_qids(f'<<lightblue>> redirects_qids:{old_q.ljust(15)} -> {new_q}.')
    for qd in mis_qids:
        print_missing_qids(f'<<lightblue>> missing_qids:{qd}.')
    printe.output(f' len of redirects_qids:  {len(redirects_qids.keys())}')
    printe.output(f' len of missing_qids:    {len(mis_qids)}')
    dump_missing_to_json(missing)
    printe.output(' log to missing.json true.... ')
    printe.output(f"{missing['all']=}")
