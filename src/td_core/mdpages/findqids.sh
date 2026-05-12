#!/bin/bash

# find_qids all
$HOME/local/bin/python3 core8/pwb.py td_core/td_other_qids/make_list all add

# find_qids td
$HOME/local/bin/python3 core8/pwb.py td_core/mdpages/find_qids redirects add

# get_red all
$HOME/local/bin/python3 core8/pwb.py td_core/db_work/get_red

# fix_qids all
$HOME/local/bin/python3 core8/pwb.py td_core/td_other_qids/fix_qids fix all

# p11143 all
$HOME/local/bin/python3 core8/pwb.py md_core/p11143_bot/bot all add addq

# unlinked_wb all
$HOME/local/bin/python3 core8/pwb.py md_core/unlinked_wb/bot


