#!/bin/bash

# all

$HOME/local/bin/python3 core8/pwb.py td_other_qids/make_list all add

# td
$HOME/local/bin/python3 core8/pwb.py mdpages/find_qids redirects add

$HOME/local/bin/python3 core8/pwb.py db_work/get_red

# other

$HOME/local/bin/python3 core8/pwb.py td_other_qids/fix_qids fix -others

# all

$HOME/local/bin/python3 core8/pwb.py td_other_qids/fix_qids fix all

$HOME/local/bin/python3 core8/pwb.py p11143_bot/bot all add addq

$HOME/local/bin/python3 core8/pwb.py unlinked_wb/bot


