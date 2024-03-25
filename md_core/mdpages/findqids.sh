#!/bin/bash

$HOME/local/bin/python3 core8/pwb.py mdpages/get_md_to_en other
$HOME/local/bin/python3 core8/pwb.py mdpages/find_qids redirects addthem
$HOME/local/bin/python3 core8/pwb.py mdpages/fixqids
$HOME/local/bin/python3 core8/pwb.py mdpages/get_red

$HOME/local/bin/python3 core8/pwb.py p11143_bot/bot --td add addq

$HOME/local/bin/python3 core8/pwb.py unlinked_wb/bot
