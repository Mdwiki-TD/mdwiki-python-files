#!/usr/bin/python3
#   himo
"""

python3 core8/pwb.py copy_data/sitelinks

"""

import sys
import tqdm
import json
import os
from apis.wd_bots.wikidataapi_post import Log_to_wiki, post_it
from newapi import printe
from mdapi_sql import sql_for_mdwiki
from mdpyget.bots.to_sql import insert_dict

if os.getenv("HOME"):
    Dashboard_path = os.getenv("HOME") + "/public_html/td"
else:
    Dashboard_path = "I:/mdwiki/mdwiki/public_html/td"

mis_qids = []

qua_1 = """
INSERT IGNORE INTO all_qids (qid)
SELECT qid FROM qids where qid != "" and qid is not null
"""

que = '''select DISTINCT qid, code from all_qidsexists;'''
# ---
in_sql = {}
# ---
for q in sql_for_mdwiki.select_md_sql(que, return_dict=True):
    qid = q["qid"]
    if qid in in_sql:
        in_sql[qid].append(q["code"])
    else:
        in_sql[qid] = [q["code"]]


def start_to_sql(data):
    # ---
    data = {q: list(v['sitelinks'].keys()) for q, v in data.items()}
    # ---
    print(data)
    # ---
    qids_list = list(data.keys())
    # ---
    if qids_list:
        qua = """
            INSERT IGNORE INTO all_qids (qid)
            values (%s)"""
        # ---
        sql_for_mdwiki.mdwiki_sql(qua, values=qids_list, many=True)
    # ---
    for qid, codes in data.items():
        # ---
        new_data = [{"qid": qid, "code": code} for code in codes if code not in in_sql.get(qid, [])]
        # ---
        printe.output(f"<<yellow>> all codes: {len(codes)}, new_data: {len(new_data)}.")
        # ---
        if new_data:
            insert_dict(new_data, "all_qidsexists", ["qid", "code"], lento=1000, title_column="qid", IGNORE=True)


def dump_sitelinks(lists):
    printe.output(f"<<green>> len of lists: {len(lists)}.")
    with open(f"{Dashboard_path}/Tables/jsons/sitelinks1.json", "w", encoding="utf-8") as aa:
        json.dump(lists, aa)


def wbgetentities(qs_list):
    # ---
    Log_to_wiki()
    # ---
    params_wd = {
        "action": "wbgetentities",
        "format": "json",
        "redirects": "yes",
        "props": "sitelinks",
        "utf8": 1,
    }
    # ---
    all_entities = {}
    # ---
    range_list = range(0, len(qs_list), 100)
    # ---
    printe.output(f"<<green>> get sitelinks for:{len(all_entities)}:")
    # ---
    for i in tqdm.tqdm(range_list):
        # ---
        qids = qs_list[i : i + 100]
        # ---
        params_wd["ids"] = "|".join(qids)
        # ---
        # printe.output(f"<<green>> done:{len(all_entities)} from {len(qs_list)}, get sitelinks for {len(qids)} qids.")
        # ---
        # json1 = wikidataapi.post(params_wd)
        json1 = post_it(params_wd)
        # ---
        if json1:
            # ---
            entities = json1.get("entities", {})
            # ---
            # {'Q133247108': {'type': 'item', 'id': 'Q133247108', 'sitelinks': {'arwiki': {'site': 'arwiki', 'title': 'تصنيف:حشرات كولومبيا', 'badges': []}, 'enwiki': {'site': 'enwiki', 'title': 'Category:Insects of Colombia', 'badges': []}}}}
            entities = json.loads(json.dumps(entities))
            # ---
            # print(entities)
            # ---
            all_entities.update(entities)
    # ---
    return all_entities


def get_qids_sitelinks(qs_list, qids_to_mdtitle={}):
    # ---
    all_entities = wbgetentities(qs_list)
    # ---
    table_d = {"heads": [], "qids": {}}
    # ---
    heads = []
    # ---
    printe.output(f"<<yellow>> {len(all_entities)=}.")
    # ---
    for qid, tab in all_entities.items():
        # ---
        if "missing" in tab:
            # ---
            mis_qids.append(tab.get("id"))
            # ---
            continue
        # ---
        qid = tab.get("id", "")
        # ---
        if qid != "" and qid not in table_d["qids"]:
            table_d["qids"][qid] = {"mdtitle": qids_to_mdtitle.get(qid, ""), "sitelinks": {}}
        # ---
        sitelinks = {}
        # ---
        # "abwiki": {"site": "abwiki","title": "Обама, Барак","badges": []}
        # ---
        for _, tab in tab.get("sitelinks", {}).items():
            # ---
            title = tab.get("title", "")
            site = tab.get("site", "")
            # ---
            if title == "" or not site.endswith("wiki"):
                continue
            # ---
            site = site[:-4]
            # ---
            sitelinks[site] = title
        # ---
        heads.extend(sitelinks.keys())
        # ---
        table_d["qids"][qid]["sitelinks"] = sitelinks
    # ---
    table_d["heads"] = list(set(heads))
    # ---
    return table_d


def main():
    # ---
    printe.output("<<green>> main")
    # ---
    qids_tab = sql_for_mdwiki.get_all_qids()
    # ---
    qids = list(qids_tab.values())
    # ---
    printe.output(f"<<green>> len of qids: {len(qids)}.")
    # ---
    qids_to_mdtitle = {qid: title for title, qid in qids_tab.items()}
    # ---
    lists = get_qids_sitelinks(qids, qids_to_mdtitle)
    # ---
    if lists:
        dump_sitelinks(lists)
        start_to_sql(lists.get("qids", {}))


def test():
    qids = ["Q133247108", "Q874563245"]
    lists = get_qids_sitelinks(qids)
    printe.output(f"<<green>> len of lists: {len(lists)}.")
    print(lists)
    start_to_sql(lists.get("qids", {}))


if __name__ == "__main__":
    if "test" in sys.argv:
        test()
    else:
        main()
