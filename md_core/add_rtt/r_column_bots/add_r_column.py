#!/usr/bin/python3
"""

from add_rtt.r_column_bots.add_r_column import add_header_R, header_has_R


"""
# ---
import wikitextparser as wtp
from newapi import printe


def header_has_R(text, table=False):
    # ---
    if not table:
        parsed = wtp.parse(text)
        table = parsed.tables[0]
    # ---
    # for table in parsed.tables:
    # ---
    for x in table.cells():
        if x[1].is_header:
            for numb, v in enumerate(x, 1):
                if v.value.strip() == "R":
                    print(f"header has R: in column {numb}")
                    return True
    # ---
    return False


def add_header_R(text, table=False):
    # ---
    if not table:
        parsed = wtp.parse(text)
        table = parsed.tables[0]
    # ---
    # for table in parsed.tables:
    # ---
    # add R to header in 2nd column
    for x in table.cells():
        if x[0].is_header:
            x[0].value = x[0].value + "\n! R"
            # print(x[0].value)
            # ---
            # print(x)
        else:
            x[0].value = x[0].value + "\n| "
            # ---
            # print(x)
    # ---
    return table.string
