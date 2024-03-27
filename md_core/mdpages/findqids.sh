#!/bin/bash

$HOME/local/bin/python3 core8/pwb.py td_other_qids/make_list -td add

$HOME/local/bin/python3 core8/pwb.py mdpages/find_qids redirects add

$HOME/local/bin/python3 core8/pwb.py mdpages/get_red

# other

$HOME/local/bin/python3 core8/pwb.py td_other_qids/make_list -others add

$HOME/local/bin/python3 core8/pwb.py td_other_qids/fix_qids fix -others

# all

$HOME/local/bin/python3 core8/pwb.py td_other_qids/fix_qids fix all

$HOME/local/bin/python3 core8/pwb.py unlinked_wb/bot all

$HOME/local/bin/python3 core8/pwb.py p11143_bot/bot all add addq
