"""
Usage:
from p11143_bot.wd_helps import fix_in_wd, add_P11143_to_qids_in_wd, make_in_wd_tab

"""
import sys
import time

from apis import wikidataapi
from newapi import printe

sys.argv.append("workhimo")

wikidataapi.Log_to_wiki(url="https://www.wikidata.org/w/api.php")


def make_in_wd_tab():
    # ---
    in_wd = {}
    # ---
    query = """select distinct ?item ?prop where { ?item wdt:P11143 ?prop .}"""
    # ---
    wdlist = wikidataapi.sparql_generator_url(query, printq=False, add_date=True)
    # ---
    for wd in wdlist:
        prop = wd["prop"]
        # ---
        qid = wd["item"].split("/entity/")[1]
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
            wikidataapi.Claim_API_str(q, "P11143", value)
            if n % 30 == 0:
                printe.output(f"<<yellow>> n: {n}")
                time.sleep(5)


def fix_in_wd(merge_qids, qids):
    # mdwiki != P11143
    # تصحيح قيم الخاصية التي لا تساوي اسم المقالة
    # ---
    for q, wd_value in merge_qids.copy().items():
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
        ase = wikidataapi.Claim_API_str(q, "P11143", md_title)
        if ase:
            print(f"True.. Added P11143:{md_title}")
        else:
            print(f"Failed to add P11143:{md_title}")
