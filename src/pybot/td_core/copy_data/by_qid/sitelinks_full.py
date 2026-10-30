#!/usr/bin/python3
"""

python c9/pwb.py td_core/copy_data/by_qid/sitelinks_full.py

"""

import json
import logging
from collections import defaultdict
from typing import Any

import requests
import tqdm
from db.mdapi_sql.sql_td_bot import tf_sql_connect_dict
from td_core.copy_data.by_qid.sitelinks_to_sql import new_to_sql

logger = logging.getLogger(__name__)

skip_codes = ["commons", "species", "ary", "arz", "meta"]

user_agent = "WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"


def get_all_qids() -> dict[str, str]:
    # ---
    query = "select DISTINCT title, qid from qids;"
    sq = tf_sql_connect_dict(query)
    return {ta["title"]: ta["qid"] for ta in sq}


def do_request(session, params: dict, method: str = "POST"):
    # ---
    url = "https://www.wikidata.org/w/api.php"
    # ---
    args = {
        "headers": {"User-Agent": user_agent},
        "timeout": 10,
    }
    # ---
    if method == "POST":
        args["data"] = params
    else:
        args["params"] = params
    # ---
    try:
        r4 = session.request(method, url, **args)
        status = r4.status_code
        # ---
        if status != 200:
            logger.error(f"<<red>> wikidataapi.py: post error status: {str(status)}")
            return {}
        # ---
        return r4.json()

    except Exception:
        logger.exception("Exception:", exc_info=True)
        return {}


def load_in_sql_qid_targets():
    # ---
    in_sql_qid_targets = defaultdict(dict)
    # ---
    que = """select DISTINCT qid, code, target from all_qids_exists;"""
    # ---
    db_data_main = tf_sql_connect_dict(que)
    # ---
    for q in db_data_main:
        qid = q["qid"]
        target = q["target"]
        lang = q["code"]
        # ----
        if target and lang:
            in_sql_qid_targets[qid][lang] = target

    logger.info(f"<<blue>> found {len(in_sql_qid_targets):,} qid in sql")
    return in_sql_qid_targets


def start_to_sql(data) -> None:
    # ---
    logger.info(f"<<green>> {len(data)=}")
    # ---
    # data = {q: list(v['sitelinks'].keys()) for q, v in data.items()}
    data = {q: v["sitelinks"] for q, v in data.items()}
    # ---
    new_data_all = []
    in_sql_qid_targets = load_in_sql_qid_targets()
    # ---
    # for qid, codes in data.items():
    for qid, sitelinks in data.items():
        # ---
        qid_in_sql = in_sql_qid_targets.get(qid, {})
        # ---
        logger.info(f"<<green>> {qid=} {len(sitelinks)=}, qid_in_sql: {len(qid_in_sql)=}")
        # ---
        new_data = [
            {"qid": qid, "code": code, "target": target}
            for code, target in sitelinks.items()
            if qid_in_sql.get(code) != target
        ]
        # ---
        if new_data:
            new_data_all.extend(new_data)
    # ---
    logger.info(f"<<yellow>> new_data_all: {len(new_data_all)}.")
    # ---
    if new_data_all:
        new_to_sql(new_data_all)


def wbgetentities(qs_list):
    # ---
    all_entities = {}
    # ---
    session = requests.Session()
    # ---
    logger.info(f" for:{len(qs_list)}:")
    # ---
    for i in tqdm.tqdm(range(0, len(qs_list), 100)):
        # ---
        qids = qs_list[i : i + 100]
        # ---
        qids = [x for x in qids if x]
        # ---
        params_wd = {
            "action": "wbgetentities",
            "format": "json",
            "redirects": "yes",
            "props": "sitelinks",
            "utf8": 1,
        }
        # ---
        params_wd["ids"] = "|".join(qids)
        # ---
        json1 = do_request(
            session=session,
            params=params_wd,
        )
        # ---
        if json1:
            # ---
            entities = json1.get("entities", {})
            # ---
            # {'Q133247108': {'type': 'item', 'id': 'Q133247108', 'sitelinks': {'arwiki': {'site': 'arwiki', 'title': 'تصنيف:حشرات كولومبيا', 'badges': []}, 'enwiki': {'site': 'enwiki', 'title': 'Category:Insects of Colombia', 'badges': []}}}}
            entities = json.loads(json.dumps(entities))
            # ---
            # logger.info(entities)
            # ---
            all_entities.update(entities)
    # ---
    logger.info(f" result: {len(all_entities)}:")
    # ---
    return all_entities


def get_qids_sitelinks(qs_list, qids_to_mdtitle=None):
    # ---
    mis_qids = []
    qids_to_mdtitle = qids_to_mdtitle or {}
    # ---
    all_entities = wbgetentities(qs_list)
    # ---
    table_d = {"heads": [], "qids": {}}
    # ---
    heads = []
    # ---
    logger.info(f"<<yellow>> {len(all_entities)=}.")
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
        qid_data = {"mdtitle": qids_to_mdtitle.get(qid, ""), "sitelinks": {}}
        # ---
        sitelinks = {}
        # ---
        # "abwiki": {"site": "abwiki","title": "Обама, Барак","badges": []}
        # ---
        for _, sub_tab in tab.get("sitelinks", {}).items():
            # ---
            title = sub_tab.get("title", "")
            site = sub_tab.get("site", "")
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
        qid_data["sitelinks"] = sitelinks
        # ---
        if qid != "" and qid not in table_d["qids"]:
            table_d["qids"][qid] = qid_data
    # ---
    table_d["heads"] = list(set(heads))
    # ---
    logger.info(f"<<yellow>> len of mis_qids: {len(mis_qids)}.")
    # ---
    return table_d


def main() -> None:
    # ---
    logger.info("<<green>> ")
    # ---
    qids_tab = get_all_qids()
    # ---
    qids = list(qids_tab.values())
    qids = list(set(qids))
    # ---
    logger.info(f"len of qids in sql: {len(qids)}, len of qids_tab: {len(qids_tab)}")
    # ---
    qids_to_mdtitle = {qid: title for title, qid in qids_tab.items()}
    # ---
    lists: dict[str, Any] = {}
    # ---
    lists = get_qids_sitelinks(qids, qids_to_mdtitle)
    # ---
    logger.info(f"len of qids from wikidata: {len(lists.get('qids', {}))}.")
    # ---
    qids_not = [x for x in qids if x not in lists.get("qids", {})]
    # ---
    logger.error(f"<<red>> len of qids_not: {len(qids_not)}")
    # ---
    for x in qids_not:
        lists["qids"][x] = {"mdtitle": qids_to_mdtitle.get(x, ""), "sitelinks": {}}
    # ---
    if lists:
        start_to_sql(lists.get("qids", {}))


if __name__ == "__main__":
    main()
