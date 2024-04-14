"""

from fix_mass.fix_sets.bots.done import studies_done_append, find_done #find_done(study_id)

"""
from pathlib import Path

Dir = Path(__file__).parent.parent

studies_done_dir = Dir / "studies_done"

def find_done(study_id):
    file = studies_done_dir / f"{study_id}.done"
    if file.exists():
        return True
    return False


def studies_done_append(study_id):
    file = studies_done_dir / f"{study_id}.done"
    if not file.exists():
        file.touch()
