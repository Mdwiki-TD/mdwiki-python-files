#!/usr/bin/python3
"""

python3 core8/pwb.py add_rtt/tests/add_r_col_to_file

"""
from newapi import printe
from pathlib import Path
from add_rtt.r_column_bots.pup_table import add_to_tables


file_path = Path(__file__).parent / "Popular_pages.txt"
file_path2 = Path(__file__).parent / "Popular_pages_new.txt"

text = file_path.read_text(encoding="utf-8")

new_text = add_to_tables(text, pages=[""])

printe.showDiff(text, new_text)

file_path2.write_text(new_text, encoding="utf-8")
