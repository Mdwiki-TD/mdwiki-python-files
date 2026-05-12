#!/bin/bash

$HOME/local/bin/python3 core8/pwb.py md_core/mdpy/fix_duplicate save

$HOME/local/bin/python3 core8/pwb.py wd_works/recheck

$HOME/local/bin/python3 core8/pwb.py db_work/check_titles

$HOME/local/bin/python3 core8/pwb.py md_core/mdpy/bots/cat_cach newlist
