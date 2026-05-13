#!/usr/bin/python3
"""
from td_core.td_dirs import paths
paths.json_files.medwiki_to_enwiki
"""

import logging
import os
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

_TABLES_PATH = os.getenv("TABLES_PATH")  # /data/project/mdwiki/public_html/td/Tables

if not _TABLES_PATH:
    raise RuntimeError("TABLES_PATH is not set")

if os.getenv("APP_ENV") == "development" and not _TABLES_PATH:
    _TABLES_PATH = "I:/MD_TOOLS/MDWIKI_MAIN_REPO/public_html/td/Tables"

_TABLES_PATH = Path(_TABLES_PATH).expanduser()


@dataclass(frozen=True)
class PathsFiles:
    all_refcount: Path
    lead_refcount: Path
    words: Path
    allwords: Path
    noqids: Path
    assessments: Path
    enwiki_pageviews: Path
    missing: Path
    sitelinks: Path
    medwiki_to_enwiki: Path


@dataclass(frozen=True)
class Paths:
    tables_path: Path
    cats_cash_path: Path
    json_tables_path: Path
    cash_exists_path: Path
    json_files: PathsFiles


_jsons_path = _TABLES_PATH / "jsons"

_json_files = PathsFiles(
    all_refcount=_jsons_path / "all_refcount.json",
    lead_refcount=_jsons_path / "lead_refcount.json",
    words=_jsons_path / "words.json",
    allwords=_jsons_path / "allwords.json",
    noqids=_jsons_path / "noqids.json",
    assessments=_jsons_path / "assessments.json",
    enwiki_pageviews=_jsons_path / "enwiki_pageviews.json",
    missing=_jsons_path / "missing.json",
    sitelinks=_jsons_path / "sitelinks.json",
    medwiki_to_enwiki=_jsons_path / "medwiki_to_enwiki.json",
)

paths = Paths(
    tables_path=_TABLES_PATH,
    json_tables_path=_jsons_path,
    cats_cash_path=_TABLES_PATH / "cats_cash",
    cash_exists_path=_TABLES_PATH / "cash_exists",
    json_files=_json_files,
)
