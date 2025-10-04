"""

python3 core8/pwb.py newupdater/tests/old_params

"""
import sys
import os
os.environ["DEBUGNEW"] = "true"

import pywikibot
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from new_updater import rename_params

o = '''
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
'''
n = rename_params(o)
# ---
pywikibot.showDiff(o, n)
