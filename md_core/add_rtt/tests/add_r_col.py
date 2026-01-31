#!/usr/bin/python3
"""

python3 core8/pwb.py add_rtt/tests/add_r_col

"""
from add_rtt.r_column_bots.pup_table import add_to_tables
from newapi import printe

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

new_text = add_to_tables(text, pages=[""])

printe.showDiff(text, new_text)
