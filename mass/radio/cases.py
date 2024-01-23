# -*- coding: utf-8 -*-
"""

python3 core8/pwb.py mass/radio/cases

Usage:

cases_file = os.path.join(str(main_dir), 'jsons/cases1.json')

with open(cases_file, 'r', encoding='utf-8') as f:
    cases_in = json.loads(f.read())

"""
import re
import os
import json
from pathlib import Path

main_dir = Path(__file__).parent

cases_file = os.path.join(str(main_dir), 'jsons/cases1.json')

if not os.path.exists(cases_file):
    with open(cases_file, 'w', encoding='utf-8') as f:
        f.write("{}")

with open(cases_file, 'r', encoding='utf-8') as f:
    cases_in = json.loads(f.read())


def geo():
    already = 0
    cases_dup = {}
    cases_in = {}
    from new_api.ncc_page import CatDepth

    cases = CatDepth('Category:Radiopaedia images by case', sitecode='www', family="nccommons", depth=0, ns="14") # 8068 cat before me

    reg = r'^Category:Radiopaedia case (\d+) (.*?)$'

    for cat in cases:
        match = re.match(reg, cat)
        if match:
            case_id = match.group(1)
            case_title = match.group(2)
            # ---
            if case_id in cases_in:
                already += 1
                print(f'already:{already}, case_id {case_id} already in cases_in ({case_title}, {cases_in[case_id]})')
            # ---
            cases_in[case_id] = case_title
            # ---
            if case_id in cases_dup:
                cases_dup[case_id].append(cat)
            else:
                cases_dup[case_id] = [cat]

    # sort cases_in by key
    cases_in = dict(sorted(cases_in.items(), key=lambda x: int(x[0])))

    # dump

    with open(cases_file, 'w', encoding='utf-8') as f:
        json.dump(cases_in, f, indent=4, ensure_ascii=False)

    print(f'lenth of cases_in: {len(cases_in)} ')

    # sort cases_dup by lenth if lenth > 1
    cases_dup = {k: v for k, v in sorted(cases_dup.items(), key=lambda item: len(item[1]), reverse=True) if len(v) > 1}
    print(f'lenth of cases_dup: {len(cases_dup)} ')

    # dump
    with open(os.path.join(str(main_dir), 'jsons/cases_dup.json'), 'w', encoding='utf-8') as f:
        json.dump(cases_dup, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    geo()
