#!/usr/bin/python3
"""

from mdcount.bots.countref_bots import count_ref_from_text

"""

from mdcount.bots.regex_scanner import RegexScanner
from newapi import printe


def get_refs_new(text):
    ref_list = []
    # ---
    scanner = RegexScanner(r"(?i)<ref(?P<name>[^>/]*)>(?P<content>.*?)</ref>", text)
    # ---
    for m in scanner.requests:
        # ---
        name = m.get("name", "")
        content = m.get("content", "")
        # ---
        if name.strip() != "":
            if name.strip() not in ref_list:
                ref_list.append(name.strip())
        elif content.strip() != "":
            if content.strip() not in ref_list:
                ref_list.append(content.strip())
    # ---
    printe.output(f"len of get_refs_new : {len(ref_list)}")
    # ---
    return ref_list


def get_short_refs(text):
    # ---
    scanner = RegexScanner(r"<ref\s*name\s*=\s*[\"\']*(?P<name>[^>]*)[\"\']*\s*\/\s*>", text)
    # ---
    ref_list = scanner.attr_scan("name")
    # ---
    # printe.output(f"len of get_short_refs : {len(ref_list)}")
    # ---
    return ref_list


def count_ref_from_text(text, get_short=False):
    # ---
    ref_list = []
    # ---
    # short_list = get_short_refs(text)
    # ---
    if get_short:
        short_list = get_short_refs(text)
        ref_list.extend(short_list)
    # ---
    refs = get_refs_new(text)
    # ---
    ref_list.extend(refs)
    # ---
    return len(ref_list)
