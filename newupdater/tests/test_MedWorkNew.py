"""

python3 core8/pwb.py newupdater/tests/test_MedWorkNew

"""
import sys
import os
import pywikibot
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
os.environ["DEBUGNEW"] = "true"

from new_updater import work_on_text

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
