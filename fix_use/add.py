"""

python3 core8/pwb.py fix_use/add path:I:/mdwiki/mdwiki/public_html/td2/actions
python3 core8/pwb.py fix_use/add path:I:/mdwiki/mdwiki/public_html/td2/enwiki

"""

import os
import sys
import logging
from pathlib import Path

if Dir := Path("I:/core/bots/"):
    sys.path.append(str(Dir))

from fix_use.bot import scan_root
from fix_use.mtab import tab
from fix_use.write_bot import write  # write(oldtext, text, filepath)

logger = logging.getLogger(__name__)

path = ""
# ---
for arg in sys.argv:
    arg, _, value = arg.partition(":")
    # ---
    if arg == "path":
        path = value.strip()


def get_adds_lines(text):
    # ---
    adds = []
    # ---
    ns_line = ""
    # ---
    for ns, functions in tab.items():
        # ---
        nsline = f"namespace {ns};"
        # ---
        if text.find(nsline) == -1:
            continue
        # ---
        ns_line = nsline
        # ---
        for func in functions:
            # ---
            r"use function Actions\HtmlSide\create_side;",
            # ---
            Add = f"use function {ns}\\{func};"
            # ---
            fo = f"function {func}("
            # ---
            if text.find(fo) == -1:
                continue
            # ---
            if text.find(Add) != -1:
                continue
            # ---
            adds.append(Add)
        # ---
        break
    # ---
    return ns_line, adds


def add_use(filepath, ns_line="", add_lines=""):
    # ---
    try:
        text = open(filepath, encoding="utf-8").read()
    except Exception as e:
        print(f"Exception : {e}")
        return
    # ---
    oldtext = text
    # ---
    if not add_lines and not ns_line:
        ns_line, add_lines = get_adds_lines(text)
    # ---
    if not add_lines:
        return
    # ---
    add_lines = "\n".join(add_lines)
    # ---
    start1 = text.rfind(f"\n{ns_line}")
    # ---
    add_lines = "\n/*\nUsage:\n\n" + add_lines + "\n\n*/\n"
    # ---
    if start1 != -1:
        # add add_lines before ns_line
        # text = text[:start1] + "\n" + add_lines + "\n\n" + text[start1:]
        # ---
        # add add_lines after ns_line
        text = text.replace(ns_line, ns_line + "\n" + add_lines, 1)
    # ---
    if oldtext != text:
        write(oldtext, text, filepath)
        oldtext = text


def start():
    logger.info(f"<<green>> fixpy: {path=}")
    # ---
    pathss = []
    # ---
    for root, dirs, files in os.walk(path, topdown=True):
        # ---
        scanroot = scan_root(root)
        # ---
        if not scanroot:
            # logger.info(f"<<green>> root: {root}.")
            continue
        # ---
        for f in files:
            # ---
            filepath = os.path.join(root, f)
            # ---
            scanit = scan_root(filepath)
            # ---
            if not scanit:
                # logger.info(f"<<green>> filepath: {filepath}.")
                continue
            # ---
            # logger.info(f"<<green>> file: {filepath}.")
            # ---
            if filepath.endswith(".php"):
                pathss.append(filepath)
    # ---
    for n, filepath in enumerate(pathss):
        logger.info(f"<<yellow>> {n}/{len(pathss)}: file: {filepath}.")
        # ---
        add_use(filepath)


if __name__ == "__main__":
    start()
