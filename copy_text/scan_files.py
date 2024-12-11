#!/usr/bin/python3
"""

python3 core8/pwb.py copy_text/scan_files


"""
import sys
import tqdm
import os
from pathlib import Path
from newapi import printe

dir1 = Path(__file__).parent
Dir = "/data/project/mdwiki/public_html/mdtexts"

if str(dir1).find("I:") != -1:
    Dir = "I:/mdwiki/mdwiki/public_html/mdtexts"

Dir = Path(Dir)

paths = [
    Dir / "html",
    Dir / "segments",
]

to_del = []

for path in paths:
    files = list(path.glob("*.html"))

    for n, file in tqdm.tqdm(enumerate(files, 1), total=len(files)):
        # printe.output(f"<<yellow>> f: {n}/{len(files)} : {file}")

        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        if text.find(">Wikimedia Error<") != -1:
            to_del.append(file)

for n, file in enumerate(to_del, 1):
    printe.output(f"<<red>> f: {n}/{len(to_del)} : Error: {file}")
    # del the file
    if "del" in sys.argv:
        os.remove(file)
    continue
