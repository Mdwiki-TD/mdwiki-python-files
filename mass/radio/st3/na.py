"""

python3 /data/project/mdwiki/pybot/mass/radio/st3/na.py test

"""

import os
import sys

from mass.radio.st3.start3 import ids_by_caseId, main

user_script_paths = [
    "I:/core/new",
    "I:/mdwiki",
    "I:/mdwiki/pybot",
    "I:/mdwiki/pybot/md_core",
    "I:/mdwiki/pybot/ncc_core",
    "/data/project/mdwiki",
    "/data/project/mdwiki/pybot",
    "/data/project/mdwiki/pybot/md_core",
    "/data/project/mdwiki/pybot/ncc_core",
]
for _u_path in user_script_paths:
    if os.path.exists(_u_path):
        sys.path.append(os.path.abspath(_u_path))

# ---
print("ids_by_caseId: ", len(ids_by_caseId))
# ---
main(ids_by_caseId)
