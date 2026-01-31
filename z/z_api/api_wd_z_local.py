"""

"""
import logging

import sys
import re
from z_api.api_wrap import session_post
from newapi import printe

logger = logging.getLogger(__name__)
Main_User = {1: ""}
Save_2020_wd = {}

fafo_rand = "960017df0e23"  # f"{random.randrange(0, 2 ** 48):x}"

summary = f"([[:toollabs:editgroups/b/CB/{fafo_rand}|details]])"

print(f"summary: {summary}")


def ask_put(s):
    yes_answer = ["y", "a", "", "Y", "A", "all", "aaa"]

    sa = input(s)
    if sa not in yes_answer:
        print(" wikidataapi: wrong answer")
        return False
    if sa == "a" or sa == "A":
        return "a"
    return True


def wbsearchentities(search, language, match_alias=False):
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "search": search,
        "language": language,
        "strictlanguage": 1,
        "limit": "max",
        "type": "item",
        "utf8": 1,
    }
    # ---
    req = session_post(params=params)
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
        if s.get("display", {}).get("label", {}).get("value", "") != "":
            table_x["label"] = s["display"]["label"]["value"]
            table_x["lang"] = s["display"]["label"]["language"]
            # ---

        elif match_one.get("type", "") == "label":
            table_x["label"] = match_one["text"]
            table_x["lang"] = match_one["language"]

        elif match_one.get("type", "") == "alias" and match_alias:
            # "match": { "type": "alias", "language": "fi", "text": "Costae" }
            table_x["label"] = match_one["text"]
            table_x["lang"] = match_one["language"]
        else:
            table_x = s
        # ---
        table[s["id"]] = table_x
    # ---
    return table


def Labels_API(Qid, label, lang, remove=False):
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
        sa = ask_put(f'<<lightyellow>> wikidataapi.py Add label:<<lightyellow>>"{lang}:{label}"<<default>> for {Qid} Yes or No ? {Main_User[1]} ')
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
    req = session_post(params=params, Type="post", addtoken=True)
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


def Des_API(Qid, desc, lang, ask="", rea=True, nowait=False):
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
        sa = ask_put(f'<<lightyellow>> wikidataapi.py Add desc:<<lightyellow>>"{lang}:{desc}"<<default>> for {Qid} Yes or No ? {Main_User[1]} ')
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
    req = session_post(params=params, Type="post", addtoken=True)
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
