# -*- coding: utf-8 -*-
"""

python3 core8/pwb.py mass/radio/cases_in_ids

"""
import re
from newapi.ncc_page import CatDepth
# ---
from mass.radio.jsons_files import jsons, dumps_jsons, ids_to_urls, urls_to_ids
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, ids=0, all_ids=0, urls_to_get_info=0)


def geo():
    print(f'lenth of jsons.cases_in_ids: {len(jsons.cases_in_ids)} ')
    already = 0

    cases = CatDepth('Category:Radiopaedia images by case', sitecode='www', family="nccommons", depth=0, ns="14") # 8068 cat before me

    reg = r'^Category:Radiopaedia case (\d+) (.*?)$'
    # ---
    new_cases_in = {}
    new_dup      = {}
    # ---
    for cat in cases:
        match = re.match(reg, cat)
        if match:
            case_id = match.group(1)
            case_title = match.group(2)
            # ---
            if case_id in new_cases_in:
                already += 1
                print(f'already:{already}, case_id {case_id} already in new_cases_in ({case_title}, {new_cases_in[case_id]})')
            # ---
            new_cases_in[case_id] = case_title
            # ---
            if case_id in jsons.cases_dup:
                jsons.cases_dup[case_id].append(cat)
            else:
                jsons.cases_dup[case_id] = [cat]

    # sort new_cases_in by key
    new_cases_in = dict(sorted(new_cases_in.items(), key=lambda x: int(x[0])))
    print(f'lenth of new_cases_in: {len(new_cases_in)} ')

    # dump
    # jsons.cases_in_ids = new_cases_in
    jsons._replace(cases_in_ids = new_cases_in)
    dumps_jsons(cases_in_ids=1)

    # sort jsons.cases_dup by lenth if lenth > 1
    new_dup = {k: v for k, v in sorted(new_dup.items(), key=lambda item: len(item[1]), reverse=True) if len(v) > 1}

    print(f'lenth of new_dup: {len(new_dup)} ')

    # dump
    # jsons.cases_dup = new_dup
    jsons._replace(cases_dup = new_dup)
    dumps_jsons(cases_dup=1)


if __name__ == "__main__":
    geo()
