#!/usr/bin/python3
"""

from add_rtt.r_column_bots.add_r_column import add_header_R, header_has_R


"""
from wikitextparser._cell import Cell
import logging

# ---
import wikitextparser as wtp

logger = logging.getLogger(__name__)


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
    # Check if R column already exists
    if header_has_R(text, table):
        logger.info("R column already exists in table header")
        return table.string
    # ---
    count = 0
    # ---
    # add R to header in 2nd column
    for x in table.cells():
        # ---
        if x[0].is_header:
            x[0].value = x[0].value + "\n! R"
        else:
            x[0].value = x[0].value + "\n| "
        # ---
        count += 1
    # ---
    logger.info(f"Added R column to table header in {count} cells")
    # ---
    return table.string
