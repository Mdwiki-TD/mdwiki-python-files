"""

from mdpages import qids_help
# qids_help.get_o_qids_new(o_qids, t_qids_in)
# qids_help.get_pages_to_work(ty="td|other")
# qids_help.check(work_list, all_pages)

"""
import json
import sys

# ---
from api_sql import sql_for_mdwiki
from api_sql import sql_qids_others
from newapi import printe
from apis import catdepth2
from apis import wiki_api
from apis import mdwiki_api
from mdpy.bots.check_title import valid_title  # valid_title(title)

# ---
from pathlib import Path

Dir = str(Path(__file__).parents[0])
# ---
dir2 = Dir.replace("\\", "/")
dir2 = dir2.split("/pybot/")[0] + "/public_html/Translation_Dashboard/Tables/jsons"
# ---
print(f"{dir2=}")


def dump_jsons(ty, medwiki_to_enwiki, missing_in_enwiki, sames):
    # ---
    if "nodump" in sys.argv:
        printe("Skipping dump of JSON files")
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
    # ---


def check(work_list, all_pages, ty):
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
    for i in range(0, len(work_list), 100):
        # ---
        group = work_list[i : i + 100]
        # ---
        params["titles"] = "|".join(group)
        # ---
        # { "error": { "code": "toomanyvalues", "info": "Too many values supplied for parameter \"titles\". The limit is 50.",
        # ---
        jsone = wiki_api.submitAPI(params, apiurl="https://en.wikipedia.org/w/api.php", returnjson=False)
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
                if red["to"] not in all_pages:
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
                if "missing" in tab:
                    missing_in_enwiki.append(title)
                else:
                    o_qids[title] = qid
                    sames.append(title)
    # ---
    for numb, (fromm, to) in enumerate(medwiki_to_enwiki.items(), start=1):
        faf = f'["{fromm}"]'
        printe.output(f'en titles {numb} from_to{faf.ljust(30)} = "{to}"')
    # ---
    for numb, mis in enumerate(missing_in_enwiki, start=1):
        printe.output(f"<<lightyellow>> {numb} title:{mis.ljust(25)} missing_in_enwiki")
    # ---
    printe.output("<<lightred>> pages both in mdwiki cat:::")
    for numb, (md, en) in enumerate(medwiki_to_enwiki_conflic.items(), start=1):
        faf = f'["{md}"]'
        fen = f'["{en}"]'
        printe.output(f"<<lightred>> {numb} page{faf.ljust(40)} to enwiki{fen}")
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
    printe.output(f"<<lightgreen>> len of medwiki_to_enwiki:{len(medwiki_to_enwiki)}")
    printe.output(f"<<lightgreen>> len of missing_in_enwiki:{len(missing_in_enwiki)}")
    printe.output(f"<<lightgreen>> len of medwiki_to_enwiki_conflic:{len(medwiki_to_enwiki_conflic)}")
    printe.output(f"<<lightgreen>> len of sames:{len(sames)}")
    printe.output(f"<<lightgreen>> len of o_qids:{len(o_qids)}")
    printe.output(f'<<lightgreen>> len of o_qids (qid != ""):{len(o_qids_n)}')
    # ---
    dump_jsons(ty, medwiki_to_enwiki, missing_in_enwiki, sames)
    # ---
    return o_qids


def get_pages_to_work(ty="td|other"):
    """
    get pages to work
    """
    # ---
    all_pages = mdwiki_api.Get_All_pages("!", namespace="0", apfilterredir="nonredirects")
    all_pages = [x for x in all_pages if valid_title(x)]
    # ---
    td_list = catdepth2.make_cash_to_cats(return_all_pages=True)
    td_list = [x for x in td_list if valid_title(x)]
    # ---
    if ty == "other":
        td_list = [x for x in all_pages if x not in td_list]
    # ---
    printe.output(f"get_pages_to_work: {len(td_list)=}, {len(all_pages)=}")
    # ---
    return td_list, all_pages


def get_o_qids_new(o_qids, t_qids_in):
    printe.output("write to sql")
    # ---
    same = [x for x in o_qids if x in t_qids_in and t_qids_in[x] == o_qids[x]]
    # ---
    diff = [x for x in o_qids if x in t_qids_in and t_qids_in[x] != o_qids[x] and o_qids[x] != "" and t_qids_in[x] != ""]
    # ---
    printe.output(f"len of same: {len(same)}")
    printe.output(f"len of diff: {len(diff)}")
    # ---
    # del all same from o_qids
    o_qids_new = {x: y for x, y in o_qids.items() if x not in same and x not in diff}
    # ---
    len_empty = [x for x in o_qids_new if o_qids_new[x] == "" and t_qids_in.get(x) == ""]
    printe.output(f"<<lightgreen>> new len of len_empty:{len(len_empty)}")
    # ---
    # del empty qids but not empty in sql qids
    for ti, q in o_qids_new.copy().items():
        if q == "" and t_qids_in.get(ti) != "":
            del o_qids_new[ti]
    # ---
    for x in diff:
        printe.output(f"x: {x}, qid_in: {t_qids_in[x]} != new qid: {o_qids[x]}")
    # ---
    return o_qids_new
