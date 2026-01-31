#!/usr/bin/python3
"""

python3 core8/pwb.py apis/wd_rest_new

from apis.wd_bots import wd_rest_new
# wd_rest_new.Get_Claims_API(q="", p="")
# wd_rest_new.Get_one_qid_info(qid, only="labels")

"""
from newapi.except_err import exception_err
import json
import logging
import sys

import requests

logger = logging.getLogger(__name__)

wd_cach = {}


def open_url_get(url):
    # ---
    result = {}
    # ---
    try:
        req = requests.get(url, timeout=10)
        result = req.json()
    except Exception as e:
        exception_err(e, text=url)
    # ---
    return result


def Get_one_qid_info(qid, only=None):
    # ---
    key_c = tuple([qid, only])
    # ---
    if key_c in wd_cach:
        return wd_cach[key_c]
    # ---
    props = ["sitelinks", "labels", "descriptions", "aliases", "statements"]
    # ---
    main_table = {
        "labels": {},
        "descriptions": {},
        "aliases": {},
        "sitelinks": {},
        "statements": {},
        "qid": qid,
    }
    # ---
    url = f"https://www.wikidata.org/w/rest.php/wikibase/v1/entities/items/{qid}"
    # ---
    if only in props:
        url += "/" + only
    # ---
    if "printurl" in sys.argv:
        logger.info(url)
    # ---
    result = open_url_get(url)
    # ---
    if only in props:
        result = {only: result}
    # ---
    main_table["labels"] = result.get("labels", {})
    main_table["descriptions"] = result.get("descriptions", {})
    main_table["aliases"] = result.get("aliases", {})
    # ---
    main_table["sitelinks"] = {x: v["title"] for x, v in result.get("sitelinks", {}).items()}
    # ---
    main_table["statements"] = result.get("statements", {})
    # ---
    # if only in props: main_table = main_table[only]
    # ---
    wd_cach[key_c] = main_table
    # ---
    return main_table


def Get_sitelinks_From_Qid(q):
    # ---
    sitelinks = Get_one_qid_info(q, only="sitelinks")
    # ---
    return sitelinks


def Get_Claims_API(q="", p=""):
    # ---
    statements = Get_one_qid_info(q, only="statements").get("statements", {})
    # ---
    logger.info(f"Get_Claims_API: {len(statements)=}")
    # ---
    claims = statements.get(p, [])
    # ---
    claims_new = []
    # ---
    for c in claims:
        claims_new.append(
            {
                "id": c.get("id", ""),
                "value": c.get("value", {}).get("content", ""),
                "rank": c.get("rank", ""),
            }
        )

    # ---
    return claims_new


if __name__ == "__main__":
    qids = ["Q26981430"]
    # ---
    for q in qids:
        logger.info(f"<<blue>>_______\n{q} :")
        # ---
        j = Get_one_qid_info(q)
        # ---
        logger.info(json.dumps(j, indent=4, ensure_ascii=False))
