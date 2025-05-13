#!/usr/bin/python3
"""

from add_rtt.r_column_bots.pup_table import add_to_tables


"""
# ---
# import re
import tqdm
import wikitextparser as wtp
from newapi import printe
from add_rtt.r_column_bots.add_r_column import add_header_R, header_has_R

R_NEW_ROW = '\n| style="text-align:center; white-space:nowrap; font-weight:bold; background:#C66A05" | R'


def fix_title(title):
    title = title.replace("[[", "").replace("]]", "")
    title = title.replace("&#039;", "'")
    # ---
    return title


def mark_as_reviewed(cell):
    cell.value = " R"
    cell.set_attr("style", "text-align:center; white-space:nowrap; font-weight:bold; background:#C66A05")  # ffd6ff


def one_cell(cell_values):
    text = "".join([x for x in cell_values])
    # ---
    text = f"{text}\n|-"
    # ---
    return text


def work_one_table(table_text, redirects, pages):
    # ---
    parsed = wtp.parse(table_text)
    table = parsed.tables[0]
    # ---
    if not header_has_R(table_text, table):
        printe.output("<<red>> no R in table header!")
        return table_text
    # ---
    already_in = []
    no_add = []
    # ---
    add_from_redirect = []
    add_done = []
    # ---
    cell_errors = []
    # ---
    data = table.data()
    # ---
    text_x = '{| class="wikitable sortable"\n'
    # ---
    for n, x in enumerate(tqdm.tqdm(table.cells())):
        # ---
        cell_values = [x.string for x in x]
        # ---
        if x[1].is_header or len(x) < 3:
            text_x += one_cell(cell_values)
            continue
        # ---
        try:
            title = x[2].value.strip()
            r_s = x[1].value.strip()
        except Exception as e:
            numb = data[n][2]
            cell_errors.append(numb)
            text_x += one_cell(cell_values)
            continue
        # ---
        title = fix_title(title)
        # ---
        title2 = redirects.get(title, title)
        # ---
        if r_s == "R":
            # mark_as_reviewed(x[1])
            # ---
            cell_values[1] = R_NEW_ROW
            # ---
            already_in.append(title)
            text_x += one_cell(cell_values)
            continue
        # ---
        # print(f"title: ({title}), r_s: ({r_s})")
        # ---
        if title in pages:
            # mark_as_reviewed(x[1])
            # ---
            cell_values[1] = R_NEW_ROW
            # ---
            add_done.append(title)
        elif title2 in pages:
            # mark_as_reviewed(x[1])
            # ---
            cell_values[1] = R_NEW_ROW
            # ---
            add_from_redirect.append(title)
        else:
            no_add.append(title)
        # ---
        text_x += one_cell(cell_values)
    # ---
    printe.output(f"<<yellow>> no_add: {len(no_add)}, already_in: {len(already_in)}")
    # ---
    printe.output(f"<<red>> cell_errors: {len(cell_errors)}:")
    printe.output(cell_errors)
    # ---
    printe.output(f"<<yellow>> add_done: {len(add_done)}, add_from_redirect: {len(add_from_redirect)}")
    # ---
    text_x += "\n|}"
    # ---
    return text_x


def add_rtt_to_tables(text, redirects={}, pages=[], table=False):
    # ---
    new_text = text
    # ---
    if not header_has_R(text, table):
        new_text = add_header_R(text, table)
        # ---
        if new_text == text:
            printe.output("<<red>> Can't add R column to table!")
            return text
    # ---
    if redirects or pages:
        new_text = work_one_table(new_text, redirects, pages)
    # ---
    return new_text


def add_to_tables(text, redirects={}, pages=[]):
    # ---
    parsed = wtp.parse(text)
    # ---
    table = parsed.tables[0]
    # ---
    table.string = add_rtt_to_tables(table.string, redirects, pages, table)
    # ---
    new_text = parsed.string
    # ---
    return new_text
