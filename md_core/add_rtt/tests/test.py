#!/usr/bin/python3
"""

python3 core8/pwb.py add_rtt/tests/test

"""
import logging

import wikitextparser as wtp

logger = logging.getLogger(__name__)

# from mdwiki_api.mdwiki_page import NEW_API
# api_new = NEW_API("www", family="mdwiki")

text = """
{| class="wikitable sortable"
! Rank
! Page title
! Views
! Daily average
! Assessment
! Importance
|-
| 1
| [[Med Jets Flight 056]]
| xx
| {{FORMATNUM:20103}}
| style="text-align:center; white-space:nowrap; font-weight:bold; background:#FFFF66" | [[:Category:C-Class articles|C]]
| style="text-align:center; white-space:nowrap; font-weight:bold; background:#ffd6ff" | [[:Category:Low-importance articles|Low]]
|-
| 2
| [[Limonene]]
| 22
| {{FORMATNUM:19568}}
| style="text-align:center; white-space:nowrap; font-weight:bold; background:#FFFF66" | [[:Category:C-Class articles|C]]
| style="text-align:center; white-space:nowrap; font-weight:bold; background:#ffd6ff" | [[:Category:Low-importance articles|Low]]
|-
|}


"""

parsed = wtp.parse(text)

for table in parsed.tables:
    # ---
    for x in table.cells():
        # ---
        # print("x[6]:", x[6])
        # ---
        r_s = x[1].value.strip()
        title = x[2].value.strip()
        # ---
        logger.info(f"<<green>> title: ({title}), r_s: ({r_s})")
        # ---
        if x[1].is_header:
            print("skip header")
            continue
        # ---
        x[1].value = "R"
        x[1].set_attr("style", "text-align:center; white-space:nowrap; font-weight:bold; background:#C66A05")  # ffd6ff

new_text = parsed.string

# titles = api_new.get_titles_redirects(["Ehlers–Danlos syndrome"]) # {'Ehlers–Danlos syndrome': 'Ehlers–Danlos syndromes'}

# print(titles)
