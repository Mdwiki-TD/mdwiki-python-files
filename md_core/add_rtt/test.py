#!/usr/bin/python3
"""

python3 core8/pwb.py add_rtt/test

"""
import wikitextparser as wtp
from newapi import printe
text = '''
{| class="wikitable sortable"
! Rank
! Page title
!R
! Views
! Daily average
! Assessment
! Importance
|-
| 1
| [[Med Jets Flight 056]]
|
| [https://pageviews.toolforge.org/?project=en.wikipedia.org&amp;start=2025-02-01&amp;end=2025-02-28&amp;pages=Med_Jets_Flight_056&amp;redirects=1 {{FORMATNUM:562910}}]
| {{FORMATNUM:20103}}
| style="text-align:center; white-space:nowrap; font-weight:bold; background:#FFFF66" | [[:Category:C-Class articles|C]]
| style="text-align:center; white-space:nowrap; font-weight:bold; background:#ffd6ff" | [[:Category:Low-importance articles|Low]]
|-
| 2
| [[Limonene]]
|
| [https://pageviews.toolforge.org/?project=en.wikipedia.org&amp;start=2025-02-01&amp;end=2025-02-28&amp;pages=Limonene&amp;redirects=1 {{FORMATNUM:547923}}]
| {{FORMATNUM:19568}}
| style="text-align:center; white-space:nowrap; font-weight:bold; background:#FFFF66" | [[:Category:C-Class articles|C]]
| style="text-align:center; white-space:nowrap; font-weight:bold; background:#ffd6ff" | [[:Category:Low-importance articles|Low]]
|-
| 3
| [[Sexual intercourse]]
|
| [https://pageviews.toolforge.org/?project=en.wikipedia.org&amp;start=2025-02-01&amp;end=2025-02-28&amp;pages=Sexual_intercourse&amp;redirects=1 {{FORMATNUM:341388}}]
| {{FORMATNUM:12192}}
| style="text-align:center; white-space:nowrap; font-weight:bold; background:#B2FF66" | [[:Category:B-Class articles|B]]
| style="text-align:center; white-space:nowrap; font-weight:bold; background:#ffc1ff" | [[:Category:Mid-importance articles|Mid]]
|-
|}


'''

parsed = wtp.parse(text)

for table in parsed.tables:
    for x in table.cells():
        title = x[1].value.strip()
        r_s = x[2].value.strip()
        print(f"title: {title}, r_s: {r_s}")
        x[2].value = "R"

new_text = parsed.string

printe.showDiff(text, new_text)
