"""

python3 core8/pwb.py fix_use/bot path:I:/mdwiki/public_html/Translation_Dashboard

"""
import json
import sys
import os
import re

sys.path.append("I:/core/bots/")
# ---
from newapi import printe
from fix_use.write_bot import write  # write(oldtext, text, filepath)
from fix_use.mtab import make_find_rep

path = ""
# ---
for arg in sys.argv:
    arg, _, value = arg.partition(":")
    # ---
    if arg == "path":
        path = value.strip()

find_rep = make_find_rep()


def scan_root(root):
    # ---
    if os.path.islink(root):
        return False
    # ---
    root = root.replace("\\", "/")
    # ---
    substrings_to_ignore = [
        "/vendor/",
        "/old/",
        "apicache-py3",
        "__pycache__",
        ".git",
        "/.",
    ]

    for substring_to_ignore in substrings_to_ignore:
        if root.find(substring_to_ignore) != -1:
            return False

    return True


def get_adds_lines(text):
    # ---
    adds = []
    # ---
    for func, Add in find_rep.items():
        # ---
        # if text has f"function {func}(" in it continue
        # ---
        fo = f"function {func}("
        if text.find(fo) != -1:
            continue
        # ---
        # find if text has "func" in it is single word
        if re.search(r"\b" + func + r"\b", text) and text.find(Add) == -1:
            adds.append(Add)
    # ---
    add_lines = "\n".join(adds)
    # ---
    return add_lines


def fix_used(filepath):
    # ---
    try:
        text = open(filepath, encoding="utf-8").read()
    except Exception as e:
        print(f"Exception : {e}")
        return
    # ---
    oldtext = text
    # ---
    add_lines = get_adds_lines(text)
    # ---
    if not add_lines:
        return
    # ---
    # add add_lines before line starts with "use" in the text
    finds = [
        r"use function ",
        r"use ",
        r"function ",
        r"include_once ",
        r"<?php\n",
    ]
    # ---
    for find in finds:
        # ---
        start1 = text.rfind(f"\n{find}")
        # ---
        if start1 != -1:
            text = text[:start1].strip() + "\n" + add_lines + "\n\n" + text[start1:].strip()
            break
    # ---
    if oldtext == text:
        text = add_lines + "\n" + text
    # ---
    if oldtext != text:
        write(oldtext, text, filepath)
        oldtext = text


def start():
    printe.output(f"<<green>> fixpy: {path=}")
    # ---
    pathss = []
    # ---
    for root, dirs, files in os.walk(path, topdown=True):
        # ---
        scanroot = scan_root(root)
        # ---
        if not scanroot:
            # printe.output(f"<<green>> root: {root}.")
            continue
        # ---
        for f in files:
            # ---
            filepath = os.path.join(root, f)
            # ---
            scanit = scan_root(filepath)
            # ---
            if not scanit:
                # printe.output(f"<<green>> filepath: {filepath}.")
                continue
            # ---
            # printe.output(f"<<green>> file: {filepath}.")
            # ---
            if filepath.endswith(".php"):
                pathss.append(filepath)
    # ---
    for n, filepath in enumerate(pathss):
        printe.output(f"<<yellow>> {n}/{len(pathss)}: file: {filepath}.")
        # ---
        fix_used(filepath)


if __name__ == "__main__":
    start()
