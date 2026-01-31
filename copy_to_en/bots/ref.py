#!/usr/bin/python3
"""
Usage:
from copy_to_en.bots.ref import fix_ref# text = fix_ref(first, alltext)
"""
# import re
import wikitextparser as wtp


def get_refs(alltext):
    """Extract reference tags from the provided text.

    This function parses the input text to identify and extract reference
    tags. It categorizes these tags into two dictionaries: one for tags that
    have associated content and another for tags that do not. The function
    ensures that only unique reference names are stored, and it strips any
    trailing slashes from the reference names.

    Args:
        alltext (str): The text containing reference tags to be parsed.

    Returns:
        tuple: A tuple containing two dictionaries:
            - ref_name_refs (dict): A dictionary mapping reference names to their
            corresponding tags that have content.
            - no_conts (dict): A dictionary mapping reference names to lists of
            tags that do not have content.
    """

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
    """Fix references in the given text by replacing short tags with full
    references.

    This function takes a string containing text with reference tags and
    another string containing all references. It parses both texts to
    identify short reference tags and their corresponding full references.
    For each short tag found in the first text that does not have a
    corresponding reference, it replaces the first occurrence of the short
    tag with the full reference from the second text. If a reference is not
    found, it prints a message indicating that the reference was not found.

    Args:
        first (str): The text containing short reference tags to be fixed.
        alltext (str): The text containing all reference definitions.

    Returns:
        str: The modified text with short reference tags replaced by full references.
    """

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
            logger.info("ref not found: " + ref_name)
            continue
        # ---
        tag_short = tags[0].string
        tag_full = contents.string
        # ---
        first = first.replace(tag_short, tag_full, 1)
    # ---
    return first
