#!/usr/bin/python3
"""

إيجاد الصفحات القديمة
تحديث صفحة User:Mr. Ibrahem/pages

python3 c8/pwb.py updates/io

"""

from apis import mdwiki_api
import sys
from pathlib import Path


Dir = Path(__file__).parent
# ---
NewList = {}
# ---
date_before_20200701 = Dir / "date_before_20200701.txt"
# ---
fakalist = []
# ---
if date_before_20200701.exists():
    fska = date_before_20200701.read_text()
    fakalist = [x.strip().split("]]")[0].replace("[[", "").strip() for x in fska.split("\n")]
# ---
listo = mdwiki_api.Get_All_pages("!", namespace="0")
listo = [x for x in listo if x not in fakalist]
if "test" in sys.argv:
    listo = listo[:100]
# ---
if "200" in sys.argv:
    listo = listo[:200]
# ---
print(f"len of listo: {len(listo)}")


def get_timestamp(titles):
    # ---
    global NewList
    # ---
    for num, page in enumerate(titles, start=1):
        params = {"action": "query", "format": "json", "prop": "revisions", "titles": page, "rvprop": "timestamp", "rvlimit": "1", "rvdir": "newer"}
        hh = mdwiki_api.post_s(params)
        # ---
        # { "action": "query", "format": "json", "prop": "revisions", "titles": "Etizolam", "utf8": 1, "rvprop": "timestamp", "rvlimit": "1", "rvdir": "newer" }
        # ---
        kk = hh.get("query", {}).get("pages", {})
        for key, vav in kk.items():
            timestamp = vav.get("revisions", [{"timestamp": ""}])[0].get("timestamp", "")
            NewList[page] = timestamp
        # ---
        if str(num).endswith("00"):
            print("page:%d:%s,timestamp:%s" % (num, page, timestamp))

        # ---


# ---
get_timestamp(listo)
# ---
laly = [[int(io.split("T")[0].replace("-", "")), x] for x, io in NewList.items() if io.split("T")[0].replace("-", "")]
laly.sort(reverse=True)
# ---
print(f"has {len(laly)} pages. ")
# ---
if not laly:
    exit()
# ---
new = [[z, g] for z, g in laly if z > 20200701]
new.sort(reverse=True)
# ---
old = [[z, g] for z, g in laly if z < 20200701]
old.sort(reverse=True)
# ---
print(f"we have {len(old)} pages with date < 20200701. ")
print(f"we have {len(new)} pages with date > 20200701. ")
# ---
masha = "\n".join([f"{s}" for d, s in new])
# ---
with open(f"{Dir}/date_after_20200701.txt", "w", encoding="utf-8") as logfil3e:
    logfil3e.write(masha)
# ---
masha3 = "\n".join([f"{ss}" for ds, ss in old])
# ---
with open(f"{Dir}/date_before_20200701.txt", "w", encoding="utf-8") as ooo:
    ooo.write(masha3)
# ---
text = f"""
* all pages: {len(laly)}
** pages with date < 20200701: {len(old)}
** pages with date > 20200701: {len(new)}
"""
text += """
--~~~~
{| class="wikitable sortable"
|-
! #
! Title
! Creation date
! Import history
"""
numb = 0
for Date, pag in new:
    numb += 1
    url = "https://" + "mdwiki.toolforge.org/import-history.php?code=James%2399&title={{urlencode:" + pag + "}}"
    text += "|-\n| %d || [[%s]] || %s || [%s ] \n" % (numb, pag, Date, url)

text += """|-
|}
"""
if "test" in sys.argv:
    print(text)
else:
    mdwiki_api.page_put(newtext=text, summary="update", title="User:Mr. Ibrahem/pages")
# ---
