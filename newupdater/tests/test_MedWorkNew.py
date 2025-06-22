"""

python3 core8/pwb.py newupdater/tests/test_MedWorkNew

"""
import sys
import os
import pywikibot
from pathlib import Path

Dir = Path(__file__).parent.parent
sys.path.append(str(Dir))
os.environ["DEBUGNEW"] = "true"

from MedWorkNew import work_on_text

with open(Dir / "bots/resources.txt", "r", encoding="utf-8") as f:
    text = f.read()
# ---
newtext = work_on_text("test", text)
# ---
if "diff" in sys.argv:
    pywikibot.showDiff(text, newtext)
else:
    print("add 'diff' to sys.argv to see diff")
# ---
with open(Dir / "bots/resources_new.txt", "w", encoding="utf-8") as f:
    f.write(newtext)
