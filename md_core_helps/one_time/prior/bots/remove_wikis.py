"""
python3 core8/pwb.py prior/remove_wikis
"""

import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


# ---
Dir = Path(__file__).parent
# ---
project_js_new = f"{Dir}/json_langs/"
project_js_newen = f"{Dir}/json_en/"
# ---
black_list = [
    "wikidata.org",
    "wikimedia.org",
    "wikipedia.org",
]


def work_in_jsfile(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    def fix_extlinks(extlinks):
        extlinks2 = extlinks
        # ---
        for oo in black_list:
            for x in extlinks:
                if x.find(oo) != -1:
                    extlinks2.remove(x)
                    continue
        # ---
        # extlinks2 = [x for x in extlinks if not any(oo in x for oo in black_list)]
        # ---
        return extlinks2

    # ---
    for title, tabs in data.items():
        if tabs.get("langs"):
            langs = tabs["langs"]
            for lang, tab in langs.items():
                # ---
                extlinks = fix_extlinks(tab["extlinks"])
                # ---
                data[title]["langs"][lang]["extlinks"] = extlinks
        # ---
        if tabs.get("extlinks"):
            extlinks = fix_extlinks(tabs["extlinks"])
            # ---
            data[title]["extlinks"] = extlinks
        # ---
        if tabs.get("lead", {}).get("extlinks"):
            extlinks = fix_extlinks(tabs["lead"]["extlinks"])
            # ---
            data[title]["lead"]["extlinks"] = extlinks
        # ---
        if tabs.get("old", {}).get("extlinks"):
            extlinks = fix_extlinks(tabs["old"]["extlinks"])
            # ---
            data[title]["old"]["extlinks"] = extlinks
        # ---
    # ---
    json.dump(data, open(filename, "w", encoding="utf-8"))

    # ---


# ---
for filename in os.listdir(project_js_new):
    if filename.endswith(".json"):
        filename2 = os.path.join(project_js_new, filename)
        # ---
        logger.info(f"filename: {filename2}..")
        # ---
        work_in_jsfile(filename2)
# ---
for filename in os.listdir(project_js_newen):
    if filename.endswith(".json"):
        filename2 = os.path.join(project_js_newen, filename)
        # ---
        logger.info(f"filename: {filename2}..")
        # ---
        work_in_jsfile(filename2)
        # ---
