# -*- coding: utf-8 -*-
"""

from new_updater import rename_params

"""

from .helps import ec_de_code, print_s
from .mv_section import move_External_links_section
from .chembox import fix_Chembox
from .bots.old_params import rename_params
from .bots.expend import expend_infoboxs_and_fix

from .MedWorkNew import work_on_text

__all__ = [
    "ec_de_code",
    "print_s",
    "work_on_text",
    "move_External_links_section",
    "fix_Chembox",
    "rename_params",
    "expend_infoboxs_and_fix",
]
