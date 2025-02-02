"""
python3 core8/pwb.py wprefs/tests/test_es/bot
"""
from wprefs.wpref_text import fix_page
from wprefs.bots.es_months import fix_es_months

import pywikibot
from pathlib import Path

Dir = Path(__file__).parent

with open(Dir / "text.txt", "r", encoding="utf-8") as f:
    text = f.read()

newtext = fix_page(text, "Demența cu corpi Lewy", move_dots=False, infobox=True, lang="es")
# newtext = fix_es_months(text)
pywikibot.showDiff(text, newtext)

with open(Dir / "text_fixed.txt", "w", encoding="utf-8") as f:
    f.write(newtext)
