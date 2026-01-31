"""

python3 core8/pwb.py newupdater/tests/mv_section Alcohol_septal_ablation

"""

import os
import sys
from pathlib import Path

import pywikibot
from mdapi import GetPageText
from new_updater import move_External_links_section

Dir = Path(__file__).parent


if Dir := Path(__file__).parent.parent:
    sys.path.append(str(Dir))


os.environ["DEBUGNEW"] = "true"


text = GetPageText(sys.argv[1])
# ---
with open(f"{Dir}/texts/section.txt", "w", encoding="utf-8") as f:
    f.write(text)
# ---
bot = move_External_links_section(str(text))
# ---
new_text = bot.make_new_txt()
# ---
pywikibot.showDiff(text, new_text)

with open(f"{Dir}/texts/secnew.txt", "w", encoding="utf-8") as f:
    f.write(new_text)
