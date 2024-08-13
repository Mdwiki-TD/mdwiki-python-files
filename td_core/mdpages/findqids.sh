#!/bin/bash

# find_qids all
$HOME/local/bin/python3 core8/pwb.py td_other_qids/make_list all add

# find_qids td
$HOME/local/bin/python3 core8/pwb.py mdpages/find_qids redirects add

# get_red all
$HOME/local/bin/python3 core8/pwb.py db_work/get_red

# fix_qids all
$HOME/local/bin/python3 core8/pwb.py td_other_qids/fix_qids fix all

# p11143 all
$HOME/local/bin/python3 core8/pwb.py p11143_bot/bot all add addq

# unlinked_wb all
$HOME/local/bin/python3 core8/pwb.py unlinked_wb/bot


