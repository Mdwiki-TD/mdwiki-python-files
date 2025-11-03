"""
Usage:
from p11143_bot.wd_helps import fix_in_wd, add_P11143_to_qids_in_wd, make_in_wd_tab

"""
import copy
import sys
import time

from apis import wikidataapi
from newapi import printe, wd_sparql

get_query_result = wd_sparql.get_query_result

sys.argv.append("workhimo")
# wikidataapi.Log_to_wiki(url="https://www.wikidata.org/w/api.php")


def make_in_wd_tab(limit=None):
    # ---
    query = """select distinct ?item ?prop where { ?item wdt:P11143 ?prop .}"""
    # ---
    if limit:
        query += f" limit {limit}"
    # ---
    wdlist = get_query_result(query)
    # ---
    in_wd = {}
    # ---
    for wd in wdlist:
        # ---
        prop = wd.get("prop", {}).get("value", "")
        # ---
        qid = wd.get("item", {}).get("value", "")
        if qid:
            qid = qid.split("/entity/")[1]
        # ---
        in_wd[qid] = prop
    # ---
    return in_wd


def add_P11143_to_qids_in_wd(newlist):
    # ---
    print(f"len of newlist: {len(newlist)}")
    # ---
    if len(newlist) > 0:
        # ---
        printe.output(f"<<yellow>>claims to add_P11143_to_qids: {len(newlist.items())}")
        if len(newlist.items()) < 100:
            print("\n".join([f"{k}\t:\t{v}" for k, v in newlist.items()]))
        # ---
        if "add" not in sys.argv:
            printe.output('<<puruple>> add "add" to sys.argv to add them?')
            return
        # ---
        for n, (q, value) in enumerate(newlist.items(), start=1):
            printe.output(f"<<yellow>> q {n} from {len(newlist)}")
            if q:
                q = q.strip()
                # wikidataapi.Claim_API_str(q, "P11143", value)
                if n % 30 == 0:
                    printe.output(f"<<yellow>> n: {n}")
                    time.sleep(5)


def fix_in_wd(merge_qids, qids):
    # mdwiki != P11143
    # تصحيح قيم الخاصية التي لا تساوي اسم المقالة
    # ---
    for q, wd_value in copy.deepcopy(merge_qids).items():
        md_title = qids.get(q)
        if md_title == wd_value:
            continue
        # ---
        print(f"wd_value:{wd_value} != md_title:{md_title}, qid:{q}")
        # ---
        merge_qids[q] = md_title
        # ---
        # delete the old
        ae = wikidataapi.Get_claim(q, "P11143", get_claim_id=True)
        if ae:
            for x in ae:
                value = x["value"]
                claimid = x["id"]
                if value == wd_value:
                    uxx = wikidataapi.Delete_claim(claimid)
                    if uxx:
                        print(f"True.. Deleted {claimid}")
                    else:
                        print(f"Failed to delete {claimid}")
        # ---

        # add the correct claim
        ase = False
        # ase = wikidataapi.Claim_API_str(q, "P11143", md_title)
        if ase:
            print(f"True.. Added P11143:{md_title}")
        else:
            print(f"Failed to add P11143:{md_title}")


if __name__ == "__main__":
    # python3 core8/pwb.py p11143_bot/wd_helps

    op = make_in_wd_tab(limit=10)
    printe.output("<<blue>>\n".join([f"{k}\t:\t{v}" for k, v in op.items()]))
