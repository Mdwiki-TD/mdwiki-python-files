"""

python3 core8/pwb.py newupdater/tests/chembox

"""

import os
import sys

os.environ["DEBUGNEW"] = "true"

from pathlib import Path

import pywikibot

sys.path.append(str(Path(__file__).parent.parent))

from new_updater import fix_Chembox

Dir = Path(__file__).parent

with open(f"{Dir}/texts/chembox.txt", "r", encoding="utf-8") as f:
    text = f.read()

bot = fix_Chembox(text)

newtext = bot.run()

pywikibot.showDiff(text, newtext)
