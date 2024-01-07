# -*- coding: utf-8 -*-
"""

python3 core8/pwb.py mass/radio/cases

Usage:

cases_file = os.path.join(str(main_dir), 'jsons/cases.json')

with open(cases_file, 'r', encoding='utf-8') as f:
    cases_in = json.loads(f.read())

"""
import re
import os
import json
from pathlib import Path

main_dir = Path(__file__).parent

cases_file = os.path.join(str(main_dir), 'jsons/cases.json')

if not os.path.exists(cases_file):
    with open(cases_file, 'w', encoding='utf-8') as f:
        f.write("{}")

with open(cases_file, 'r', encoding='utf-8') as f:
    cases_in = json.loads(f.read())

def geo():
    cases_in = {}
    from new_api.ncc_page import CatDepth
    cases = CatDepth('Category:Radiopaedia images by case', sitecode='www', family="nccommons", depth=0, ns="14")

    reg = r'^Category:Radiopaedia case (\d+) (.*?)$'

    for cat in cases:
        match = re.match(reg, cat)
        if match:
            case_id = match.group(1)
            case_title = match.group(2)
            if case_id in cases_in:
                print(f'case_id {case_id} already in cases_in ({case_title}, {cases_in[case_id]})')
            cases_in[case_id] = case_title

    # sort cases_in by key
    cases_in = dict(sorted(cases_in.items(), key=lambda x: int(x[0])))

    # dump

    with open(cases_file, 'w', encoding='utf-8') as f:
        json.dump(cases_in, f, indent=4, ensure_ascii=False)

    print(f'lenth of cases_in: {len(cases_in)} ')

if __name__ == "__main__":
    geo()