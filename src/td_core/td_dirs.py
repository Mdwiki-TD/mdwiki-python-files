#!/usr/bin/python3
"""
from td_core.td_dirs import paths
TABLES_PATH = paths.tables_path
"""

import logging
import os
from dataclasses import dataclass


logger = logging.getLogger(__name__)

TABLES_PATH = os.getenv("TABLES_PATH")  # /data/project/mdwiki/public_html/td/Tables

if not TABLES_PATH:
    TABLES_PATH = "I:/MD_TOOLS/MDWIKI_MAIN_REPO/public_html/td/Tables"


@dataclass(frozen=True)
class Paths:
    tables_path: str


paths = Paths(
    tables_path=TABLES_PATH,
)
