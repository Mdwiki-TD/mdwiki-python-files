"""
python3 core8/pwb.py fix_cs1/bot

"""
import re
import sys

import wikitextparser as wtp
from newapi import printe

from fix_cs1.bots.find_journal import get_journal_value, get_param
from fix_cs1.bots.temps_list import in_params_en, in_params_ar

def fix_one_temp(temp, find_params):
    # ---
    for param in find_params:
        va = get_param(temp, param)
        if va:
            # printe.output(f"** temp has |{param} = {va}")
            return temp
    # ---
    journal = get_journal_value(temp)
    # ---
    if journal:
        temp.set_arg("journal", journal)
    # else:
    #     printe.output("Journal value not found for template.")
    #     printe.output(temp)
    # ---
    return temp


def get_temps(parsed, valid_list):
    # ---
    Template_list = []
    # ---
    for tempa in parsed.templates:
        # ---
        temp_str = tempa.string
        # ---
        if not temp_str or temp_str.strip() == "":
            continue
        # ---
        name = str(tempa.normal_name()).strip()
        # ---
        if name.lower() not in valid_list:
            continue
        # ---
        Template_list.append(tempa)
    # ---
    printe.output(f"** result totall reftemps is: {len(Template_list)} ")
    # ---
    return Template_list


def fix_it(text, site=""):
    # ---
    ref_temps_n = ["cite journal", "cite magazine", "استشهاد بمجلة", "استشهاد بدورية محكمة"]
    # ---
    find_params = in_params_ar if site == "ar" else in_params_en
    # ---
    newtext = text
    # ---
    parsed = wtp.parse(text)
    # ---
    temps = get_temps(parsed, ref_temps_n)
    # ---
    for temp in temps:
        temp = fix_one_temp(temp, find_params)
    # ---
    newtext = parsed.string
    # ---
    return newtext
