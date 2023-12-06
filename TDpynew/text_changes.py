"""
python3 core8/pwb.py TDpynew/text_changes

Usage:
from TDpynew import text_changes
"""
from TDpynew import printe
import wikitextparser as wtp
# ---
temps_to_delete = [
    "short description", 
    "toc limit", 
    'use american english', 
    'use dmy dates', 
    'sprotect', 
    'about', 
    'featured article', 
    'redirect',
    '#unlinkedwikibase'
    ]


def work(text):
    # ---
    parsed = wtp.parse(text)
    for temp in parsed.templates:
        # ---
        name = str(temp.normal_name()).strip()
        if name.lower() in temps_to_delete:
            text = text.replace(temp.string.strip(), '')
    # ---
    parsed = wtp.parse(text)
    # ---
    for func in parsed.parser_functions:
        name = func.name
        # ---
        if name.lower() in temps_to_delete:
            text = text.replace(func.string.strip(), '')
    # ---
    return text.strip()

if __name__ == '__main__':
    tet = """"""
    #---
    newtext = work(tet)
    printe.showDiff(tet, newtext)
    #---