"""

from fix_mass.fix_sets.lists.studies_fixed import studies_fixed_done

"""
import re
from newapi.ncc_page import CatDepth

studies_fixed_done = []

cat = CatDepth("Category:Sort studies fixed", sitecode="www", family="nccommons", depth=0, only_titles=True)
no_match = []

for x in cat:
    ma = re.search(r"\(Radiopaedia (\d+)-(\d+) ", x) or re.search(r"id: (\d+) study: (\d+)", x)
    if not ma:
        no_match.append(x)
        continue
    # ---
    study_id = ma.group(2)
    # ---
    studies_fixed_done.append(study_id)
# ---
print(f"studies_fixed_done: {len(studies_fixed_done):,}")
