#!/usr/bin/python3
"""

python3 core8/pwb.py copy_text/scan_files


"""
import logging
import os
import sys
from pathlib import Path

import tqdm

logger = logging.getLogger(__name__)

dir1 = Path(__file__).parent
Dir = "/data/project/medwiki/public_html/mdtexts"

if str(dir1).find("I:") != -1:
    Dir = "I:/medwiki/new/medwiki.toolforge.org_repo/public_html/mdtexts"

Dir = Path(Dir)

paths = [
    Dir / "html",
    Dir / "segments",
]

to_del = []

for path in paths:
    files = list(path.glob("*.html"))

    for n, file in tqdm.tqdm(enumerate(files, 1), total=len(files)):
        # logger.info(f"<<yellow>> f: {n}/{len(files)} : {file}")

        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        if text.find(">Wikimedia Error<") != -1:
            to_del.append(file)

for n, file in enumerate(to_del, 1):
    logger.error(f"<<red>> f: {n}/{len(to_del)} : Error: {file}")
    # del the file
    if "del" in sys.argv:
        os.remove(file)
    continue
