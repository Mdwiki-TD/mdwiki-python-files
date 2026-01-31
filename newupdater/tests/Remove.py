"""

python3 core8/pwb.py newupdater/tests/Remove

"""

from new_updater.bots.Remove import portal_remove, remove_cite_web
import os
import sys
from pathlib import Path

import pywikibot


if Dir := Path(__file__).parent.parent:
    sys.path.append(str(Dir))

os.environ["DEBUGNEW"] = "true"


Dir = Path(__file__).parent.parent

remove_cite_web("temptext", {}, "", "")

text = "{{portal bar|Medicine}}"

new_text = portal_remove(text)

pywikibot.showDiff(text, new_text)
