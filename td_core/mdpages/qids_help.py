"""

from mdpages import qids_help
# qids_help.get_o_qids_new(o_qids, t_qids_in)
# qids_help.get_pages_to_work(ty="td|other")
# qids_help.check(work_list, all_pages)

"""

import copy
import json
import logging
import os
import re
import sys

from apis import cat_cach, mdwiki_api, wiki_api
from mdpy.bots.check_title import valid_title

logger = logging.getLogger(__name__)

if os.getenv("HOME"):
    Dashboard_path = os.getenv("HOME") + "/public_html/td"
else:
    Dashboard_path = "I:/mdwiki/mdwiki/public_html/td"
# ---
dir2 = Dashboard_path + "/Tables/jsons"

logger.info("Get_All_pages:")
# ---
all_pages = mdwiki_api.Get_All_pages("!", namespace="0", apfilterredir="nonredirects")
all_pages = [x for x in all_pages if valid_title(x)]
# ---
logger.info("make_cash_to_cats:")
# ---
td_list = cat_cach.from_cache()
td_list = [x for x in td_list if valid_title(x)]
# ---


def get_pages_to_work(ty="td|other"):
    """
    get pages to work
    """
    # ---
    global td_list
    # ---
    tds_list = td_list
    # ---
    if ty == "other":
        tds_list = [x for x in all_pages if x not in tds_list]
    # ---
    logger.info(f": {len(tds_list)=}, {len(all_pages)=}")
    # ---
    return tds_list, all_pages


def dump_jsons(ty, medwiki_to_enwiki, missing_in_enwiki, sames):
    # ---
    if "nodump" in sys.argv:
        logger.info("Skipping dump of JSON files")
        return
    # ---
    json_ext = "_other.json" if "other" == ty else ".json"
    # ---
    with open(f"{dir2}/medwiki_to_enwiki{json_ext}", "w", encoding="utf-8") as aa:
        json.dump(medwiki_to_enwiki, aa)
    # ---
    with open(f"{dir2}/missing_in_enwiki{json_ext}", "w", encoding="utf-8") as bb:
        json.dump(missing_in_enwiki, bb)
    # ---
    with open(f"{dir2}/sames{json_ext}", "w", encoding="utf-8") as cc:
        json.dump(sames, cc)


def check(work_list, all_xpages, ty):
    """
    function retrieves QIDs for a list of items. It uses the MediaWiki API to query for page properties and extracts the Wikidata item property. The function handles redirects and normalizes the titles. It also groups the items into batches of 50 to avoid exceeding the API's limit for the number of titles in a single request. This is a good practice for working with APIs.
    """
    # ---
    sames = []
    medwiki_to_enwiki = {}
    medwiki_to_enwiki_conflic = {}
    # ---
    missing_in_enwiki = []
    # ---
    o_qids = {}
    # ---
    params = {
        "action": "query",
        "format": "json",
        "prop": "info|pageprops",
        "ppprop": "wikibase_item",
        "redirects": 1,
        "rdlimit": "max",
        # "titles": line,
        "converttitles": 1,
        "utf8": 1,
    }
    # ---
    # if "redirects" in sys.argv:
    #     params["redirects"] = 1
    #     params["rdlimit"] = "max"
    # ---
    for i in range(0, len(work_list), 50):
        # ---
        group = work_list[i : i + 50]
        group = [re.sub(r"^Video:", "Wikipedia:VideoWiki/", x, flags=re.IGNORECASE) for x in group]
        # ---
        params["titles"] = "|".join(group)
        # ---
        # { "error": { "code": "toomanyvalues", "info": "Too many values supplied for parameter \"titles\". The limit is 50.",
        # ---
        jsone = wiki_api.submitAPI(params, site="en", returnjson=False)
        # ---
        if jsone and "batchcomplete" in jsone:
            # ---
            query = jsone.get("query", {})
            # ---
            redirects_x = {x["to"]: x["from"] for x in query.get("redirects", [])}
            # ---
            # "redirects": [{"from": "Acetylsalicylic acid","to": "Aspirin"}]
            Redirects = query.get("redirects", [])
            for red in Redirects:
                if red["to"] not in all_xpages:
                    medwiki_to_enwiki[red["from"]] = red["to"]
                else:
                    medwiki_to_enwiki_conflic[red["from"]] = red["to"]
            # ---
            # "pages": { "4195": {"pageid": 4195,"ns": 0,"title": "Aspirin","redirects": [{"pageid": 4953,"ns": 0,"title": "Acetylsalicylic acid"}]} }
            pages = query.get("pages", {})
            # ---
            # { "-1": { "ns": 0, "title": "Fsdfdsf", "missing": "" }, "2767": { "pageid": 2767, "ns": 0, "title": "ACE inhibitor" } }
            # ---
            for _, tab in pages.items():
                # ---
                title = tab.get("title", "")
                # ---
                qid = tab.get("pageprops", {}).get("wikibase_item", "")
                # ---
                title = redirects_x.get(title, title)
                # ---
                title = title.replace("Wikipedia:VideoWiki/", "Video:")
                # ---
                if "missing" in tab:
                    missing_in_enwiki.append(title)
                else:
                    o_qids[title] = qid
                    sames.append(title)
    # ---
    if medwiki_to_enwiki:
        logger.info("<<yellow>> en titles medwiki_to_enwiki:")
        for numb, (fromm, to) in enumerate(medwiki_to_enwiki.items(), start=1):
            faf = f'["{fromm}"]'
            logger.info(f'\t {numb} from_to{faf.ljust(30)} = "{to}"')
    # ---
    if missing_in_enwiki:
        logger.info("<<yellow>> titles missing_in_enwiki:")
        for numb, mis in enumerate(missing_in_enwiki, start=1):
            logger.info(f"\t <<yellow>>{numb}\t{mis.ljust(25)}")
    # ---
    if medwiki_to_enwiki_conflic:
        logger.info("<<red>> pages both in mdwiki cat:::")
        for numb, (md, en) in enumerate(medwiki_to_enwiki_conflic.items(), start=1):
            faf = f'["{md}"]'
            fen = f'["{en}"]'
            logger.info(f"\t <<red>> {numb} page{faf.ljust(40)} to enwiki{fen}")
    # ---
    sames = list(set(sames))
    missing_in_enwiki = list(set(missing_in_enwiki))
    # ---
    o_qids_n = {x: q for x, q in o_qids.items() if q != ""}
    # ---
    for x in missing_in_enwiki:
        if x not in o_qids:
            o_qids[x] = ""
    # ---
    logger.info(f"<<green>> len of medwiki_to_enwiki: {len(medwiki_to_enwiki):,}")
    logger.info(f"<<green>> len of missing_in_enwiki: {len(missing_in_enwiki):,}")
    logger.info(f"<<green>> len of medwiki_to_enwiki_conflic: {len(medwiki_to_enwiki_conflic):,}")
    logger.info(f"<<green>> len of sames: {len(sames):,}")
    logger.info(f"<<green>> len of o_qids: {len(o_qids):,}")
    logger.info(f'<<green>> len of o_qids (qid != ""): {len(o_qids_n):,}')
    # ---
    dump_jsons(ty, medwiki_to_enwiki, missing_in_enwiki, sames)
    # ---
    return o_qids


def get_o_qids_new(o_qids, t_qids_in):
    # logger.info("write to sql")
    # ---
    same = [x for x in o_qids if x in t_qids_in and t_qids_in[x] == o_qids[x]]
    # ---
    diff = [
        x for x in o_qids if x in t_qids_in and t_qids_in[x] != o_qids[x] and o_qids[x] != "" and t_qids_in[x] != ""
    ]
    # ---
    logger.info(f"o_qids_new: len of same: {len(same)}")
    # ---
    # del all same from o_qids
    o_qids_new = {x: y for x, y in o_qids.items() if x not in same and x not in diff}
    # ---
    len_empty = [x for x in o_qids_new if o_qids_new[x] == "" and t_qids_in.get(x) == ""]
    logger.info(f"<<green>> new len of len_empty: {len(len_empty)}")
    # ---
    # del empty qids but not empty in sql qids
    for ti, q in copy.deepcopy(o_qids_new).items():
        if q == "" and t_qids_in.get(ti) != "":
            del o_qids_new[ti]
    # ---
    logger.info(f"o_qids_new: len of diff: {len(diff)}")
    # ---
    if diff:
        logger.info("<<purple>> diff:")
        # ---
        for x in diff:
            logger.info(f"\t x: {x}, qid_in: {t_qids_in[x]} != new qid: {o_qids[x]}")
    # ---
    return o_qids_new
