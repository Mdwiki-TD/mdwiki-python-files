"""

python3 core8/pwb.py newupdater/tests/old_params

"""

import os
import sys

os.environ["DEBUGNEW"] = "true"

from pathlib import Path

import pywikibot

sys.path.append(str(Path(__file__).parent.parent))

from new_updater import rename_params

o = """
{{drugbox
|side effects=test
<!-- asdadsxxx -->

|temp = {{sub
|side effects=test1<!-- asdads -->
}}
}}
{{infobox drug
|side effects=22
|side effects=211
}}
"""
n = rename_params(o)
# ---
pywikibot.showDiff(o, n)
