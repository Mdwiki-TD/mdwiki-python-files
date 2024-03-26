#!/bin/bash

$HOME/local/bin/python3 core8/pwb.py mdpy/fix_duplicate save

$HOME/local/bin/python3 core8/pwb.py mdpy/recheck

$HOME/local/bin/python3 core8/pwb.py mdpy/check_titles

$HOME/local/bin/python3 core8/pwb.py mdpy/bots/catdepth2 newlist