"""

python3 core8/pwb.py newupdater/tests/chembox

"""

import sys
import os

os.environ["DEBUGNEW"] = "true"

import pywikibot
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from new_updater import fix_Chembox

Dir = Path(__file__).parent

with open(f"{Dir}/texts/chembox.txt", "r", encoding="utf-8") as f:
    text = f.read()

bot = fix_Chembox(text)

newtext = bot.run()

pywikibot.showDiff(text, newtext)
