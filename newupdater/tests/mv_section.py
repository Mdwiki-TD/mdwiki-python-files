"""

python3 core8/pwb.py newupdater/tests/mv_section Alcohol_septal_ablation

"""
import sys
import os

import pywikibot
from pathlib import Path

Dir = Path(__file__).parent

sys.path.append(str(Path(__file__).parent.parent))

os.environ["DEBUGNEW"] = "true"

from newupdater import mv_section
from newupdater.med import GetPageText

text = GetPageText(sys.argv[1])
# ---
with open(f"{Dir}/texts/section.txt", "w", encoding="utf-8") as f:
    f.write(text)
# ---
bot = mv_section.move_External_links_section(str(text))
# ---
new_text = bot.make_new_txt()
# ---
pywikibot.showDiff(text, new_text)

with open(f"{Dir}/texts/secnew.txt", "w", encoding="utf-8") as f:
    f.write(new_text)
