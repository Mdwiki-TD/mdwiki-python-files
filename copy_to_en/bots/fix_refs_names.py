#!/usr/bin/python3
"""
Usage:
from copy_to_en.bots.fix_refs_names import fix_ref_names

python3 core8/pwb.py copy_to_en/bots/fix_refs_names

"""
import logging

import wikitextparser as wtp

logger = logging.getLogger(__name__)


def fix_ref_names(text):
    parsed_page = wtp.parse(text)

    ref_tags = parsed_page.get_tags("ref")

    #  <ref name=Stat2022> to: <ref name="Stat2022">

    for tag in ref_tags:
        if not tag.contents:
            continue
        # ---
        for x in tag.attrs:
            u = tag.get_attr(x)
            tag.set_attr(x, u)
    # ---
    new_text = parsed_page.string
    # ---
    return new_text
