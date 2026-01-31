"""

python3 core8/pwb.py newupdater/tests/test_mdapi Alcohol_septal_ablation

"""

import os
import sys
from pathlib import Path


if Dir := Path(__file__).parent.parent:
    sys.path.append(str(Dir))


os.environ["DEBUGNEW"] = "true"

from mdapi import GetPageText

title = sys.argv[1] if len(sys.argv) > 1 else "Retinol"

text = GetPageText(title)

print(f"title: {title}")

print(f"text: {text}")
