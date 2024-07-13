#!/usr/bin/python3
"""
Usage:
from copy_to_en.ref import fix_ref# text = fix_ref(first, alltext)
"""
import re

ref_complite = re.compile(r"(<ref\s*name\s*\=*\s*[\"\']*([^>]*)[\"\']*\s*>[^<>]+</ref>)")
ref_short = re.compile(r"(<ref\s*name\s*\=\s*[\"\']*([^>]*)[\"\']*\s*\/\s*>)")


def get_full_refs(alltext):
    refs = {}
    # ---
    for m in ref_complite.finditer(alltext):
        name3 = re.sub(r"\s*\"$", "", m.group(2)).strip()
        if name3 != "":
            refs[name3] = m.group()
    return refs


def get_short_refs(first):
    short_refs = {}
    # ---
    for g in ref_short.finditer(first):
        refe = g.group()
        # ---
        name = g.group(2).strip()
        name = re.sub(r"\s*\"$", "", name)
        name = name.strip()
        # ---
        if name == "":
            continue
        # ---
        short_refs[name] = refe
    # ---
    return short_refs

def fix_ref(first, alltext):
    first = first
    # ---
    refs = get_full_refs(alltext)
    # ---
    short_refs = get_short_refs(first)
    # ---
    for name, refe in short_refs.items():
        rr = refs.get(name, False)
        # ---
        if rr:
            first = first.replace(refe, rr)
        else:
            # empty ref
            first = first.replace(refe, "")
    # ---
    return first

