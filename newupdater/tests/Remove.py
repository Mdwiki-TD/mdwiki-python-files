"""

python3 core8/pwb.py newupdater/tests/Remove

"""
import sys
import os
import pywikibot
from pathlib import Path

Dir = Path(__file__).parent.parent
sys.path.append(str(Dir))
os.environ["DEBUGNEW"] = "true"

from newupdater.bots.Remove import remove_cite_web, portal_remove

remove_cite_web("temptext", {}, "", "")

text = "{{portal bar|Medicine}}"

new_text = portal_remove(text)

pywikibot.showDiff(text, new_text)
