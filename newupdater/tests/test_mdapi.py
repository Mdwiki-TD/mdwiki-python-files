"""

python3 core8/pwb.py newupdater/tests/test_mdapi Alcohol_septal_ablation

"""
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

os.environ["DEBUGNEW"] = "true"

from mdapi import GetPageText

title = sys.argv[1] if len(sys.argv) > 1 else "Retinol"

text = GetPageText(title)

print(f"title: {title}")

print(f"text: {text}")
