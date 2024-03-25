#!/usr/bin/python3
"""
بوت يجمع بين وظيفة بوتين:
* mdpages/get_md_to_en
* mdpages/find_qids

"""
# python3 core8/pwb.py mdpages/qids/make_list
# python3 core8/pwb.py mdpages/qids/make_list add_sql
# python3 core8/pwb.py mdpages/qids/make_list add_sql add
import sys

# ---
from mdpy.bots import sql_for_mdwiki
from mdpy.bots import catdepth2
from mdpy.bots import wiki_api
from mdpy import printe
from mdpy.bots.check_title import valid_title  # valid_title(title)
from unlinked_wb.bot import work_un_linked_wb  # (title, qid)

# ---
medwiki_to_enwiki_conflic = {}
medwiki_to_enwiki = {}
# ---
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# sql_for_mdwiki.add_titles_to_qids(tab, add_empty_qid=False)
# sql_for_mdwiki.set_title_where_qid(new_title, qid)


def work_un(tab):
    for numb, (title, new_q) in enumerate(tab.items(), start=1):
        # ---
        printe.output(f"<<yellow>> work_un: {numb}, {title=}, {new_q=}")
        # ---
        if new_q:
            work_un_linked_wb(title, new_q)


def add_sql(o_qids):
    printe.output("write to sql")
    # ---
    t_qids_in = sql_for_mdwiki.get_all_qids()
    # t_qids_in = { x: y for x, y in t_qids_in.items() if y != ''}
    # ---
    same = [x for x in o_qids if x in t_qids_in and t_qids_in[x] == o_qids[x]]
    # ---
    # diff = [x for x in o_qids if x in t_qids_in and t_qids_in[x] != o_qids[x] and o_qids[x] != '']
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
    # del empty qids but not empty in get_all_qids
    for ti, q in o_qids_new.copy().items():
        if q == "" and t_qids_in.get(ti) != "":
            del o_qids_new[ti]
    # ---
    for x in diff:
        printe.output(f"x: {x}, qid_in: {t_qids_in[x]} != new qid: {o_qids[x]}")
    # ---
    printe.output(f'<<lightgreen>> new len of o_qids_new:{len(o_qids_new)}, add "add" to sys.argv to add to sql')
    # ---
    if "add" in sys.argv:
        sql_for_mdwiki.add_titles_to_qids(o_qids_new, add_empty_qid=True)
    # ---
    work_un(o_qids_new)


def check():
    """
    function retrieves QIDs for a list of items. It uses the MediaWiki API to query for page properties and extracts the Wikidata item property. The function handles redirects and normalizes the titles. It also groups the items into batches of 50 to avoid exceeding the API's limit for the number of titles in a single request. This is a good practice for working with APIs.
    """
    # ---
    sames = []
    missing_in_enwiki = []
    # ---
    o_qids = {}
    # ---
    printe.output("Get all pages...")
    # ---
    Listo = catdepth2.make_cash_to_cats(return_all_pages=True)
    # ---
    printe.output(f"len of cats pages: {len(Listo)}")
    # ---
    Listo = [x for x in Listo if valid_title(x)]
    # ---
    params = {
        "action": "query",
        "format": "json",
        # "redirects": 1,
        "prop": "pageprops",
        "ppprop": "wikibase_item",
        "converttitles": 1,
        "utf8": 1,
    }
    # ---
    if "redirects" in sys.argv:
        params["redirects"] = 1
    # ---
    num = 0
    # ---
    for i in range(0, len(Listo), 100):
        # ---
        group = Listo[i : i + 100]
        # ---
        params["titles"] = "|".join(group)
        # ---
        jsone = wiki_api.submitAPI(params, apiurl="https://en.wikipedia.org/w/api.php", returnjson=False)
        # ---
        if jsone and "batchcomplete" in jsone:
            query = jsone.get("query", {})
            # ---
            redirects_x = {x["to"]: x["from"] for x in query.get("redirects", [])}
            # ---
            # "redirects": [{"from": "Acetylsalicylic acid","to": "Aspirin"}]
            Redirects = query.get("redirects", [])
            for red in Redirects:
                if red["to"] not in Listo:
                    medwiki_to_enwiki[red["from"]] = red["to"]
                else:
                    medwiki_to_enwiki_conflic[red["from"]] = red["to"]
            # ---
            # "pages": { "4195": {"pageid": 4195,"ns": 0,"title": "Aspirin","redirects": [{"pageid": 4953,"ns": 0,"title": "Acetylsalicylic acid"}]} }
            pages = query.get("pages", {})
            # ---
            # { "-1": { "ns": 0, "title": "Fsdfdsf", "missing": "" }, "2767": { "pageid": 2767, "ns": 0, "title": "ACE inhibitor" } }
            # ---
            for _, kk in pages.items():
                # ---
                num += 1
                # ---
                title = kk.get("title", "")
                qid = kk.get("pageprops", {}).get("wikibase_item", "")
                # ---
                title = redirects_x.get(title, title)
                # ---
                if "missing" in kk:
                    missing_in_enwiki.append(title)
                else:
                    o_qids[title] = qid
                    sames.append(title)
    # ---
    numb = 0
    for fromm, to in medwiki_to_enwiki.items():
        numb += 1
        faf = f'["{fromm}"]'
        printe.output(f'en titles {numb} from_to{faf.ljust(30)} = "{to}"')
    # ---
    numb = 0
    # ---
    printe.output("<<lightred>> pages both in mdwiki cat:::")
    for md, en in medwiki_to_enwiki_conflic.items():
        numb += 1
        faf = f'["{md}"]'
        fen = f'["{en}"]'
        printe.output(f"<<lightred>> {numb} page{faf.ljust(40)} to enwiki{fen}")
    # ---
    sames = list(set(sames))
    missing_in_enwiki = list(set(missing_in_enwiki))
    # ---
    printe.output(f"<<lightgreen>> len of medwiki_to_enwiki:{len(medwiki_to_enwiki)}")
    printe.output(f"<<lightgreen>> len of missing_in_enwiki:{len(missing_in_enwiki)}")
    printe.output(f"<<lightgreen>> len of medwiki_to_enwiki_conflic:{len(medwiki_to_enwiki_conflic)}")
    printe.output(f"<<lightgreen>> len of sames:{len(sames)}")
    # ---
    printe.output(f"<<lightgreen>> len of o_qids:{len(o_qids)}")
    # --
    o_qids_n = {x: q for x, q in o_qids.items() if q != ""}
    printe.output(f'<<lightgreen>> len of o_qids (qid != ""):{len(o_qids_n)}')
    # ---
    for x in missing_in_enwiki:
        if not x in o_qids:
            o_qids[x] = ""
    # ---
    o_qids = {x: v for x, v in o_qids.items() if x in Listo}
    # ---
    # write to sql
    add_sql(o_qids)
    # ---


if __name__ == "__main__":
    check()
