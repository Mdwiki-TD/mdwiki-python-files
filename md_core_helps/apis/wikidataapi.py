#!/usr/bin/python3
"""

بوت للعمل على ويكيبيانات أو ويكيبيديا

from apis import wikidataapi
# q = wikidataapi.new_item(label="", lang="", returnid=True)

python3 core8/pwb.py apis/wikidataapi

"""
import re
import sys
import json

# ---
from newapi import printe
from apis.wd_bots import wd_rest_new

from apis.wd_bots.wikidataapi_post import post_it

# from apis.wd_bots.wd_post_new import post_it

Main_User = {1: ""}
Save_2020_wd = {}


def ask_put(s):
    yes_answer = ["y", "a", "", "Y", "A", "all", "aaa"]

    sa = input(s)
    if sa not in yes_answer:
        print(" wikidataapi: wrong answer")
        return False
    if sa == "a" or sa == "A":
        return "a"
    return True


def post(params, token=True):
    return post_it(params=params, token=token)


def Get_sitelinks_From_Qid(q):
    return wd_rest_new.Get_sitelinks_From_Qid(q)


def Get_claim(q, pid, get_claim_id=False):
    return wd_rest_new.Get_Claims_API(q=q, p=pid)


def WD_Merge(q1, q2):
    # ---
    q11 = re.sub(r"Q", "", q1)
    q22 = re.sub(r"Q", "", q2)
    # ---
    if q11.isdigit() and q22.isdigit():
        # ---
        if int(q11) > int(q22):
            From = q1
            To = q2
        else:
            From = q2
            To = q1
    else:
        From = q2
        To = q1
    # ---
    printe.output(f"from {From} to {To} ")
    # ---
    params = {
        "action": "wbmergeitems",
        "fromid": From,
        "toid": To,
        "ignoreconflicts": "description",
        "summary": "",
    }
    # ---
    r4 = post_it(params=params, token=True)
    # ---
    if not r4:
        return False
    # ---
    if "success" in r4:
        if '"redirected":1' in r4:
            printe.output("<<green>> ** true .. redirected.")
            return True
        else:
            printe.output("<<green>> ** true.")
            # ---
            pams2 = {
                "action": "wbcreateredirect",
                "from": From,
                "to": To,
                "ignoreconflicts": "description",
                "summary": "",
            }
            # ---
            r5 = post_it(params=pams2, token=True)
            # ---
            if "success" in r5:
                printe.output("<<green>> **createredirect true.")
                return True
            else:
                printe.output(f"<<red>> r5{str(r5)}")
    else:
        printe.output(f"<<red>> r4{str(r4)}")
        return False


def Labels_API(Qid, label, lang, remove=False, summary=""):
    # ---
    if not Qid:
        printe.output("Labels_API Qid == '' ")
        return False
    # ---
    if label == "" and not remove:
        printe.output("Labels_API label == '' and remove = False ")
        return False
    # ---
    # save the edit
    _out = f'{Qid} label:"{lang}"@{label}.'
    # ---
    Save_2020_wd.setdefault("labels", False)
    # ---
    if not Save_2020_wd["labels"] and "ask" in sys.argv:
        # ---
        sa = ask_put(
            f'<<lightyellow>> wikidataapi.py Add label:<<lightyellow>>"{lang}:{label}"<<default>> for {Qid} Yes or No ? {Main_User[1]} '
        )
        # ---
        if not sa:
            return False
        # ---
        if sa == "a":
            printe.output("<<lightgreen>> ----------------------------------------------")
            printe.output("<<lightgreen>> wikidataapi.py Labels_API save without asking.")
            printe.output("<<lightgreen>> ----------------------------------------------")
            Save_2020_wd["labels"] = True
    # ---
    params = {
        "action": "wbsetlabel",
        "id": Qid,
        "language": lang,
        "value": label,
        "summary": summary,
    }
    # ---
    req = post_it(params=params, token=True)
    # ---
    if req:
        text = str(req)
        if ("using the same description text" in text) and ("associated with language code" in text):
            # item2 = re.search(r'(Q\d+)', str(req["error"]['info'])).group(1)
            match = re.search(r"(Q\d+)", str(req["error"]["info"]))
            item2 = match.group(1) if match else "Unknown"
            printe.output(f"<<red>>API: same label item: {item2}")
        # ---
        if "success" in req:
            printe.output("<<green>> **Labels_API true.")
            return True
        else:
            printe.output(f"<<red>> r5{str(req)}")
    # ---
    return False


def Des_API(Qid, desc, lang, ask="", rea=True, nowait=False, summary=""):
    # ---
    if not desc.strip():
        printe.output("<<red>> Des_API desc is empty.")
        return
    # ---
    # save the edit
    _out = f'def Des_API: {Qid} description:"{lang}"@{desc}'
    # ---
    Save_2020_wd.setdefault("descriptions", False)
    # ---
    if not Save_2020_wd["descriptions"] and (ask is True or "ask" in sys.argv):
        # ---
        sa = ask_put(
            f'<<lightyellow>> wikidataapi.py Add desc:<<lightyellow>>"{lang}:{desc}"<<default>> for {Qid} Yes or No ? {Main_User[1]} '
        )
        if not sa:
            return False
        # ---
        if sa == "a":
            printe.output("<<lightgreen>> ---------------------------------")
            printe.output("<<lightgreen>> wikidataapi.py save all without asking.")
            printe.output("<<lightgreen>> ---------------------------------")
            Save_2020_wd["descriptions"] = True
    # ---
    params = {
        "action": "wbsetdescription",
        "id": Qid,
        "language": lang,
        "value": desc,
        "summary": summary,
    }
    # ---
    req = post_it(params=params, token=True)
    # ---
    if not req:
        return False
    # ---
    if "success" in req:
        printe.output("<<green>> **Labels_API true.")
        return True
    else:
        printe.output(f"<<red>> r5{str(req)}")
    # ---


def get_redirects(liste):
    # ---
    if not liste:
        return {}
    # ---
    redirects = {}
    # ---
    # print(liste)
    # ---
    for i in range(0, len(liste), 50):
        # ---
        group = []
        # ---
        if isinstance(liste, list):
            group = liste[i : i + 50]
        elif isinstance(liste, dict):
            group = list(liste.keys())[i : i + 50]
        # ---
        group = [x for x in group if x]
        # ---
        titles_line = "|".join(group)
        # ---
        params = {
            "action": "query",
            "format": "json",
            "titles": titles_line,
            "redirects": 1,
            "utf8": 1,
        }
        # ---
        json1 = post_it(params=params, token=True)
        # ---
        if json1:
            redd = json1.get("query", {}).get("redirects", [])
            for red in redd:
                redirects[red["from"]] = red["to"]
    return redirects


def new_item(label="", lang="", summary="", returnid=False):
    # ---
    data = {"labels": {lang: {"language": lang, "value": label}}}
    # ---
    params = {
        "action": "wbeditentity",
        "new": "item",
        "summary": summary,
        "data": json.JSONEncoder().encode(data),
        "format": "json",
    }
    # ---
    req = post_it(params=params, token=True)
    # ---
    if not req:
        printe.output(f"req:str({req})")
        return False
    # ---
    if "success" not in req:
        printe.output(f"<<red>> req{str(req)}")
        return False
    # ---
    printe.output("<<green>> **Claim_API true.")
    # ---
    if returnid:
        # ---
        Qid = False
        # ---
        if "entity" in req and "id" in req["entity"]:
            Qid = req["entity"]["id"]
            printe.output(f'<<green>> new_item returnid:"{Qid}" ')
        # ---
        return Qid
    # ---
    return True


def Claim_API_str(qid, property, string):
    """Add a claim to a specified QID in the API.

    This function constructs a request to add a claim to a given QID using
    the specified property and string value. It first checks if any of the
    input parameters are empty and returns an empty string if so. If the
    parameters are valid, it sends a request to the API and processes the
    response. The function logs the process and returns a boolean indicating
    the success of the operation.

    Args:
        qid (str): The QID to which the claim is being added.
        property (str): The property under which the claim is categorized.
        string (str): The value of the claim being added.

    Returns:
        bool: True if the claim was successfully added, False otherwise.
            An empty string is returned if any input parameter is empty.
    """

    # ---
    qid = qid.strip()
    # ---
    printe.output(f"<<yellow>> Claim_API_str: add claim to qid: {qid}, [{property}:{string}]")
    # ---
    if string == "" or qid == "" or property == "":
        return ""
    # ---
    params = {
        "action": "wbcreateclaim",
        "entity": qid,
        "snaktype": "value",
        "property": property,
        "value": json.JSONEncoder().encode(string),
    }
    # ---
    if property == "P11143":
        params["summary"] = "([[:toollabs:editgroups/b/CB/p11143000|details]])"
    # ---
    req = post_it(params=params, token=True)
    # ---
    if not req:
        printe.output(f"req:str({req})")
        return False
    # ---
    if "success" in req:
        printe.output("<<green>> **Claim_API true.")
        return True
    else:
        printe.output(f"<<red>> req{str(req)}")
    # ---
    return False


def Delete_claim(claimid):
    # ---
    params = {"action": "wbremoveclaims", "claim": claimid}
    # ---
    req = post_it(params=params, token=True)
    # ---
    if not req:
        printe.output(f"req:str({req})")
        return False
    # ---
    if "success" in req:
        printe.output("<<green>> **Claim_API true.")
        return True
    else:
        printe.output(f"<<red>> req{str(req)}")
    # ---
    return False


def wbsearchentities(search, language, match_alias=False):
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "search": search,
        "language": language,
        "strictlanguage": 1,
        "type": "item",
        "utf8": 1,
    }
    # ---
    req = post_it(params=params)
    # ---
    if not req:
        printe.output(" wbsearchentities no req ")
        return False
    # ---
    if "success" not in req:
        printe.output(f"<<red>> wbsearchentities: {str(req)}")
        return False
    # ---
    table = {}
    # ---
    search_table = req.get("search", [])
    # ---
    for s in search_table:
        _ss = {
            "id": "Q111587429",
            "title": "Q111587429",
            "pageid": 106531075,
            "display": {"label": {"value": "User:Mr. Ibrahem/Sodium nitrite (medical use)", "language": "en"}},
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q111587429",
            "concepturi": "http://www.wikidata.org/entity/Q111587429",
            "label": "User:Mr. Ibrahem/Sodium nitrite (medical use)",
            "match": {"type": "label", "language": "en", "text": "User:Mr. Ibrahem/Sodium nitrite (medical use)"},
        }
        # ---
        table_x = {}
        # ---
        match_one = s.get("match", {})
        # ---
        match_one_text = match_one.get("text", "")
        # ---
        if match_one_text.lower() == search.lower():
            if match_one.get("type", "") == "label":
                table_x["label"] = match_one_text
                table_x["lang"] = match_one["language"]

            elif match_one.get("type", "") == "alias" and match_alias:
                # "match": { "type": "alias", "language": "fi", "text": "Costae" }
                table_x["label"] = match_one_text
                table_x["lang"] = match_one["language"]
        # ---
        if not table_x and s.get("display", {}).get("label", {}).get("value", "") != "":
            table_x["label"] = s["display"]["label"]["value"]
            table_x["lang"] = s["display"]["label"]["language"]
        # ---
        table[s["id"]] = table_x or s
    # ---
    return table


if __name__ == "__main__":
    qids = ["Q4115189"]
    # ---
    for q in qids:
        printe.output(f"<<blue>>_______\n{q} :")
        # ---
        q = q.strip()
        # ---
        j = wd_rest_new.Get_Claims_API(q=q, p="P11143")
        # ---
        printe.output(json.dumps(j, indent=4))
        # ---
        uu = Claim_API_str(qid=q, property="P11143", string="test")
        # ---
        printe.output(uu)
        # ---
        oo = Labels_API(q, "tesst!", "en")
        # ---
        oo = Labels_API(q, "تجربة!", "ar")
        # ---
        oo = Labels_API(q, "تجربة!", "axxr")
