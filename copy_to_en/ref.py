#!/usr/bin/python3
"""
Usage:
from copy_to_en.ref import fix_ref# text = fix_ref(first, alltext)
"""
# import re
import wikitextparser as wtp


def get_refs(alltext, get_non=False):
    parsed_page = wtp.parse(alltext)

    ref_tags = parsed_page.get_tags("ref")

    ref_name_refs = {}
    no_conts = {}

    # Iterate over each ref tag
    for tag in ref_tags:
        # Check if the tag already has a group attribute
        if tag.has_attr("group"):
            continue
        # ---
        ref_name = tag.get_attr("name")
        # ---
        if not tag.contents:
            if ref_name:
                no_conts.setdefault(ref_name, []).append(tag)
            continue
        # ---
        if ref_name in ref_name_refs:
            continue
        # ---
        ref_name_refs[ref_name] = tag
    if get_non:
        return no_conts
    return ref_name_refs


def fix_ref(first, alltext):
    # Parse the page text using wikitextparser
    ref_name_refs = get_refs(alltext)

    first_name_refs = get_refs(first, get_non=True)

    # Iterate over each ref tag
    for ref_name, tags in first_name_refs.items():
        # ---
        contents = ref_name_refs.get(ref_name)
        # ---
        if not contents:
            continue
        # ---
        tag_short = tags[0].string
        tag_full = contents.string
        # ---
        first = first.replace(tag_short, tag_full, 1)
    # ---
    return first
