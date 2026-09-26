#!/bin/bash

$HOME/local/bin/python3 c9/pwb.py md_core/mdpy/fix_duplicate save

$HOME/local/bin/python3 c9/pwb.py td_core/wd_works/recheck

$HOME/local/bin/python3 c9/pwb.py td_core/db_work/check_titles

$HOME/local/bin/python3 c9/pwb.py md_core/mdpy/bots/cat_cach newlist
