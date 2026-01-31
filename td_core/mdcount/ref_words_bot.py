#!/usr/bin/python3
"""

from mdcount.ref_words_bot import get_jsons, logaa, make_old_values, do_to_sql

"""

import json

from mdapi_sql import sql_for_mdwiki
from mdpyget.bots.to_sql import to_sql
from newapi import printe


def do_to_sql(data_all, data_lead, ty="ref"):
    if ty == "ref":
        table = "refs_counts"
        title_c = "r_title"
        all_c = "r_all_refs"
        lead_c = "r_lead_refs"
    elif ty == "word":
        table = "words"
        title_c = "w_title"
        all_c = "w_all_words"
        lead_c = "w_lead_words"
    # ---
    data2 = [{title_c: x, lead_c: v, all_c: data_all.get(x, 0)} for x, v in data_lead.items()]
    # ---
    to_sql(data2, table, [title_c, lead_c, all_c], title_column=title_c)


def make_old_values(all_data, lead_data):
    # ---
    # list for titles in both all_data and lead_data
    old_values = list(set(all_data.keys()) & set(lead_data.keys()))
    # ---
    # remove duplicates from list
    old_values = list(set(old_values))
    # ---
    list_ma = [x for x in old_values if (x in all_data and (x in lead_data))]
    # ---
    list_ma.extend([x for x in all_data.keys() if (x not in list_ma and x.lower().startswith("video:"))])
    # ---
    return list_ma


def logaa(file, table):
    with open(file, "w", encoding="utf-8") as outfile:
        json.dump(table, outfile, sort_keys=True, indent=2)
    # ---
    printe.output(f"<<green>> {len(table)} lines to {file}")


def check_it(x, y, old_values):
    # ---
    if not old_values.get(x):
        return True
    # ---
    if old_values.get(x) == 0:
        return True
    # ---
    # return x not in old_values or not old_values.get(x)
    return False


def get_data(file, ty_data):
    # ---
    with open(file, "r", encoding="utf-8") as f:
        js_data = json.load(f)
        js_data = {x: ref for x, ref in js_data.items() if check_it(x, ref, ty_data)}
        # ---
        for x, y in js_data.items():
            ty_data[x] = y
    # ---
    return ty_data


def get_jsons_new(file_all, file_lead, ty):
    # ---
    if ty == "ref":
        table = "refs_counts"
        title_c = "r_title"
        all_c = "r_all_refs"
        lead_c = "r_lead_refs"
    elif ty == "word":
        table = "words"
        title_c = "w_title"
        all_c = "w_all_words"
        lead_c = "w_lead_words"
    # ---
    que = f"select DISTINCT {title_c}, {lead_c}, {all_c} from {table}"
    # ---
    in_sql = sql_for_mdwiki.mdwiki_sql_dict(que)
    # ---
    ty_all_data = {x[title_c]: x[all_c] for x in in_sql}  # if x[all_c] > 0 and x[title_c] not in ty_all_data}
    # ---
    all_data = get_data(file_all, ty_all_data)
    # ---
    ty_lead_data = {x[title_c]: x[lead_c] for x in in_sql}  # if x[lead_c] > 0 and x[title_c] not in ty_data}
    # ---
    lead_data = get_data(file_lead, ty_lead_data)
    # ---
    printe.output(f"len of lead_data:{len(lead_data.keys())}, all :{len(all_data.keys())}")
    # ---
    # sort lead_data by name
    lead_data = {k: lead_data[k] for k in sorted(lead_data)}
    all_data = {k: all_data[k] for k in sorted(all_data)}
    # ---
    return all_data, lead_data


def get_jsons(file_all, file_lead, ty):
    # ---
    if ty == "ref":
        table = "refs_counts"
        title_c = "r_title"
        all_c = "r_all_refs"
        lead_c = "r_lead_refs"
    elif ty == "word":
        table = "words"
        title_c = "w_title"
        all_c = "w_all_words"
        lead_c = "w_lead_words"
    # ---
    que = f"select DISTINCT {title_c}, {lead_c}, {all_c} from {table}"
    # ---
    in_sql = sql_for_mdwiki.mdwiki_sql_dict(que)
    # ---
    all_data = {x[title_c]: x[all_c] for x in in_sql}  # if x[all_c] > 0 and x[title_c] not in all_data}
    # ---
    lead_data = {x[title_c]: x[lead_c] for x in in_sql}  # if x[lead_c] > 0 and x[title_c] not in lead_data}
    # ---
    with open(file_all, "r", encoding="utf-8") as f:
        js_alldata = json.load(f)
        js_alldata = {x: ref for x, ref in js_alldata.items() if check_it(x, ref, all_data)}
        # ---
        for x, y in js_alldata.items():
            all_data[x] = y
    # ---
    with open(file_lead, "r", encoding="utf-8") as f:
        js_leaddata = json.load(f)
        js_leaddata = {x: ref for x, ref in js_leaddata.items() if check_it(x, ref, lead_data)}
        # ---
        for x, y in js_leaddata.items():
            lead_data[x] = y
    # ---
    printe.output(f"len of lead_data:{len(lead_data.keys())}, all :{len(all_data.keys())}")
    # ---
    # sort lead_data by name
    lead_data = {k: lead_data[k] for k in sorted(lead_data)}
    all_data = {k: all_data[k] for k in sorted(all_data)}
    # ---
    return all_data, lead_data
