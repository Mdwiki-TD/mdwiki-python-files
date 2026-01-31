"""

python3 core8/pwb.py newupdater/tests/test_MedWorkNew

"""

from new_updater import work_on_text
import os
import sys
from pathlib import Path

import pywikibot


if Dir := Path(__file__).parent.parent:
    sys.path.append(str(Dir))

os.environ["DEBUGNEW"] = "true"


Dir = Path(__file__).parent

with open(Dir / "texts/1/resources.txt", "r", encoding="utf-8") as f:
    text = f.read()
# ---
newtext = work_on_text("test", text)
# ---
if "diff" in sys.argv:
    pywikibot.showDiff(text, newtext)
else:
    print("add 'diff' to sys.argv to see diff")
# ---
with open(Dir / "texts/1/resources_new.txt", "w", encoding="utf-8") as f:
    f.write(newtext)
