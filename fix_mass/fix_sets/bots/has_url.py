"""

from fix_mass.fix_sets.bots.has_url import has_url_append

"""

import os
from pathlib import Path

Dir = Path(__file__).parent.parent

studies_has_url_dir = Dir / "has_url"
if not studies_has_url_dir.exists():
    studies_has_url_dir.mkdir()

already_has_url = [x.replace(".h", "") for x in os.listdir(studies_has_url_dir)]


def find_has_url(study_id):
    file = studies_has_url_dir / f"{study_id}.h"
    if file.exists():
        return True
    return False


def has_url_append(study_id):
    file = studies_has_url_dir / f"{study_id}.h"
    if not file.exists():
        file.touch()
