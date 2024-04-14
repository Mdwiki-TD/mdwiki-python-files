"""

from fix_mass.fix_sets.bots.has_url import has_url_append

"""
from pathlib import Path

Dir = Path(__file__).parent.parent

studies_done_dir = Dir / "has_url"
if not studies_done_dir.exists():
    studies_done_dir.mkdir()

def has_url_append(study_id):
    file = studies_done_dir / f"{study_id}.h"
    if not file.exists():
        file.touch()
