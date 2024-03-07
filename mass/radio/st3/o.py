"""
python3 core8/pwb.py mass/radio/st3/o 176190
"""
"""Script for dealing with Radiopaedia case operations

This script is used to handle operations related to Radiopaedia cases.
"""

# Script for handling Radiopaedia operation tasks
import sys
import sys
from mass.radio.st3.start3 import main_by_ids
# ---
from mass.radio.st3.start3 import main_by_ids
# ---
ids = [arg for arg in sys.argv[1:] if arg.isdigit()]
# ---
print(f"len ids: {len(ids)}")
# ---
main_by_ids(ids)
# ---
