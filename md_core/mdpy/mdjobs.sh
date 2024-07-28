#!/bin/bash

$HOME/local/bin/python3 core8/pwb.py mdpy/fix_duplicate save

$HOME/local/bin/python3 core8/pwb.py mdpy/recheck

$HOME/local/bin/python3 core8/pwb.py db_work/check_titles

$HOME/local/bin/python3 core8/pwb.py mdpy/bots/cat_cach newlist
