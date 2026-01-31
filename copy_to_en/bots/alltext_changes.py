"""
python3 core8/pwb.py copy_to_en/bots/alltext_changes

Usage:
from copy_to_en import alltext_changes

"""

import logging
import re

import wikitextparser as wtp
from copy_to_en.bots import text_changes

logger = logging.getLogger(__name__)


def change_last_Section(section):
    # del all categories
    text = section.contents
    # ---
    for cat in section.wikilinks:
        # print(cat)
        if str(cat).startswith("[[Category:"):
            text = text.replace(str(cat), "")

    text = re.sub(r"\n+", "\n", text)

    # del all langlinks

    for line in text.split("\n"):
        line2 = line.strip()
        pattern = r"\[\[[a-z-]+:[^\]\n]+\]\]"
        matches = re.findall(pattern, line2)
        for m in matches:
            text = text.replace(m, "")

    return text


def do_alltext_changes(text):
    parsed = wtp.parse(text)
    # get the last Section
    last_Section = ""
    for section in reversed(parsed.sections):
        last_Section = section
        break

    last_new = change_last_Section(last_Section)

    text = text.replace(last_Section.contents, last_new)

    return text


def do_all_text(alltext, revid, unlinkedwikibase):
    # ---
    revid_temp = f"{{{{mdwiki revid|{revid}}}}}"
    # ---
    alltext = text_changes.do_text_fixes(alltext)
    # ---
    alltext = do_alltext_changes(alltext)
    # ---
    alltext += "\n[[Category:Mdwiki Translation Dashboard articles/fulltext]]"
    # ---
    alltext = f"{unlinkedwikibase}\n{revid_temp}\n{alltext}"
    # ---
    return alltext


if __name__ == "__main__":
    # python3 core8/pwb.py copy_to_en/tests/test_alltext_changes
    tet = """"""
    # ---
    newtext = do_alltext_changes(tet)
    printe.showDiff(tet, newtext)
    # ---
