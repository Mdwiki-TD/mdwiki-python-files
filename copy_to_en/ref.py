#!/usr/bin/python3
"""
Usage:
from copy_to_en.ref import fix_ref# text = fix_ref(first, alltext)
"""
# import re
import wikitextparser as wtp


def get_refs(alltext):
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
        if ref_name:
            ref_name = ref_name.strip()
            if ref_name.endswith("/"):
                ref_name = ref_name[:-1]
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
    # ---
    return ref_name_refs, no_conts


def fix_ref(first, alltext):
    # Parse the page text using wikitextparser
    all_name_refs, all_non = get_refs(alltext)

    first_name_refs, first_non = get_refs(first)

    # Iterate over each ref tag
    for ref_name, tags in first_non.items():
        # ---
        if first_name_refs.get(ref_name):
            continue
        # ---
        contents = all_name_refs.get(ref_name)
        # ---
        if not contents:
            print("ref not found: " + ref_name)
            continue
        # ---
        tag_short = tags[0].string
        tag_full = contents.string
        # ---
        first = first.replace(tag_short, tag_full, 1)
    # ---
    return first
