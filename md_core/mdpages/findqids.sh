#!/bin/bash

$HOME/local/bin/python3 core8/pwb.py td_other_qids/make_list -td add

$HOME/local/bin/python3 core8/pwb.py mdpages/get_md_to_en

$HOME/local/bin/python3 core8/pwb.py mdpages/find_qids redirects add

$HOME/local/bin/python3 core8/pwb.py td_other_qids/fix_qids fix -td

$HOME/local/bin/python3 core8/pwb.py mdpages/get_red

$HOME/local/bin/python3 core8/pwb.py p11143_bot/bot -td add addq

$HOME/local/bin/python3 core8/pwb.py unlinked_wb/bot


# other

$HOME/local/bin/python3 core8/pwb.py td_other_qids/make_list -others add

$HOME/local/bin/python3 core8/pwb.py mdpages/get_md_to_en -others

$HOME/local/bin/python3 core8/pwb.py td_other_qids/fix_qids fix -others

$HOME/local/bin/python3 core8/pwb.py p11143_bot/bot -others add addq
