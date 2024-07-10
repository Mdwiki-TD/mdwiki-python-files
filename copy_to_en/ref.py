#!/usr/bin/python3
"""
Usage:
from copy_to_en.ref import fix_ref# text = fix_ref(first, alltext)
"""
import re

ref_complite = re.compile(r"(<ref\s*name\s*\=*\s*[\"\']*([^>]*)[\"\']*\s*>[^<>]+</ref>)")
ref_short = re.compile(r"(<ref\s*name\s*\=\s*[\"\']*([^>]*)[\"\']*\s*\/\s*>)")


def fix_ref(first, alltext):
    first = first
    # ---
    refs = {}
    # ---
    for m in ref_complite.finditer(alltext):
        refec = m.group()

        name3 = re.sub(r"\s*\"$", "", m.group(2)).strip()

        if name3 != "":
            refs[name3] = refec
    # ---
    for g in ref_short.finditer(first):
        refe = g.group()
        # ---
        name = g.group(2).strip()
        name = re.sub(r"\s*\"$", "", name)
        name = name.strip()
        # ---
        rr = refs.get(name, False)
        if name != "" and rr:
            first = first.replace(refe, rr)
    # ---
    return first
