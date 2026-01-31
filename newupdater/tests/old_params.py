"""

python3 core8/pwb.py newupdater/tests/old_params

"""

from new_updater import rename_params
import pywikibot
from pathlib import Path
import os
import sys

os.environ["DEBUGNEW"] = "true"




if Dir := Path(__file__).parent.parent:
    sys.path.append(str(Dir))



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
