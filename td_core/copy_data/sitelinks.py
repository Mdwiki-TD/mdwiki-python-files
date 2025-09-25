#!/usr/bin/python3
#   himo
"""

python3 core8/pwb.py copy_data/sitelinks

(all_qids_titles|all_qids_exists|all_qids)
(all_exists|all_articles_titles|all_articles|all_qids_titles|all_qids_exists|all_qids)
"""

import sys
import tqdm
import json
import os
from apis.wd_bots.wikidataapi_post import Log_to_wiki, post_it
from newapi import printe
from mdapi_sql import sql_for_mdwiki
from mdapi_sql import sql_for_mdwiki_new
# from mdpyget.bots.to_sql import insert_dict, to_sql
from mdpyget.bots.to_sql_new import new_to_sql
# ---
if os.getenv("HOME"):
    Dashboard_path = os.getenv("HOME") + "/public_html/td"
else:
    Dashboard_path = "I:/mdwiki/mdwiki/public_html/td"
# ---
# json_file = f"{Dashboard_path}/Tables/jsons/sitelinks1.json"
json_file = f"{Dashboard_path}/Tables/jsons/sitelinks.json"
# ---
skip_codes = ["commons", "species", "ary", "arz", "meta"]
# ---
qua_1 = """
INSERT IGNORE INTO all_qids (qid)
SELECT qid FROM qids where qid != "" and qid is not null
"""
# ---
mis_qids = []
in_sql = {}
# ---
que = '''select DISTINCT qid, code, target from all_qids_exists;'''
# ---
for q in sql_for_mdwiki_new.select_md_sql(que, return_dict=True):
    qid = q["qid"]
    if qid in in_sql:
        in_sql[qid].append(q["code"])
    else:
        in_sql[qid] = [q["code"]]


def start_to_sql(data):
    # ---
    printe.output(f"<<green>> start_to_sql {len(data)=}")
    # ---
    # data = {q: list(v['sitelinks'].keys()) for q, v in data.items()}
    data = {q: v["sitelinks"] for q, v in data.items()}
    # ---
    # print(data)
    # ---
    qids_list = list(data.keys())
    # ---
    if qids_list:
        qua = """
            INSERT IGNORE INTO all_qids (qid)
            values (%s)"""
        # ---
        sql_for_mdwiki_new.mdwiki_sql(qua, values=qids_list, many=True)
    # ---
    # for qid, codes in data.items():
    for qid, sitelinks in data.items():
        # ---
        # new_data = [{"qid": qid, "code": code} for code in codes if code not in in_sql.get(qid, [])]
        new_data = [
            {"qid": qid, "code": code, "target": target}
            for code, target in sitelinks.items()
            # if code not in in_sql.get(qid, [])
        ]
        # ---
        if new_data:
            # ---
            columns = ["qid", "code", "target"]
            # ---
            printe.output(f"<<yellow>> all sitelinks: {len(sitelinks)}, new_data: {len(new_data)}.")
            # ---
            # insert_dict(new_data, "all_qids_exists", columns, lento=1000, title_column="qid", IGNORE=True)
            new_to_sql(new_data, "all_qids_exists", columns, title_columns=["qid", "code"], update_columns=["target"], IGNORE=True)


def dump_sitelinks(lists):
    printe.output(f"<<green>> dump_sitelinks, len of qids: {len(lists.get('qids', {}))}.")
    with open(json_file, "w", encoding="utf-8") as aa:
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
    printe.output(f"wbgetentities for:{len(qs_list)}:")
    # ---
    for i in tqdm.tqdm(range(0, len(qs_list), 100)):
        # ---
        qids = qs_list[i : i + 100]
        # ---
        qids = [x for x in qids if x]
        # ---
        params_wd["ids"] = "|".join(qids)
        # ---
        # printe.output(f"done:{len(all_entities)} from {len(qs_list)}, get sitelinks for {len(qids)} qids.")
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
    printe.output(f"wbgetentities result: {len(all_entities)}:")
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
            if site in skip_codes or site[:-4] in skip_codes:
                continue
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
    printe.output(f"<<yellow>> len of mis_qids: {len(mis_qids)}.")
    # ---
    return table_d


def main():
    # ---
    printe.output("<<green>> main")
    # ---
    qids_tab = sql_for_mdwiki.get_all_qids()
    # ---
    qids = list(qids_tab.values())
    qids = list(set(qids))
    # ---
    printe.output(f"len of qids in sql: {len(qids)}, len of qids_tab: {len(qids_tab)}")
    # ---
    qids_to_mdtitle = {qid: title for title, qid in qids_tab.items()}
    # ---
    lists = {}
    # ---
    if "json" in sys.argv:
        with open(json_file, "r", encoding="utf-8") as aa:
            lists = json.load(aa)
        # ---
        printe.output(f"len of qids in json file: {len(lists.get('qids', {}))}.")
    else:
        # ---
        lists = get_qids_sitelinks(qids, qids_to_mdtitle)
        # ---
        printe.output(f"len of qids from wikidata: {len(lists.get('qids', {}))}.")
    # ---
    qids_not = [x for x in qids if x not in lists.get("qids", {})]
    # ---
    printe.output(f"<<red>> len of qids_not: {len(qids_not)}")
    # ---
    for x in qids_not:
        lists["qids"][x] = {"mdtitle": qids_to_mdtitle.get(x, ""), "sitelinks": {}}
    # ---
    if lists:
        dump_sitelinks(lists)
        start_to_sql(lists.get("qids", {}))


def test():
    qids = ["Q84263196", "Q805"]
    lists = get_qids_sitelinks(qids)
    printe.output(f"len of lists: {len(lists)}.")
    print(lists)
    start_to_sql(lists.get("qids", {}))


if __name__ == "__main__":
    if "test" in sys.argv:
        test()
    else:
        main()
