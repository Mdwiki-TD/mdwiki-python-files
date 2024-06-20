#!/bin/bash
# fix cases
python3 core8/pwb.py mass/radio/st3/start3  ask noapi  get:1 allids del2 updatetext


python3 core8/pwb.py mass/radio/st3/o2 del2 nomulti ask

# then fix studies
python3 core8/pwb.py fix_mass/fix_sets/o

# work all
python3 core8/pwb.py mass/radio/st3/start3 ask noapi get:1 allids del2 updatetext

tfj run cdcd --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/start3 noapi get:1 allids del2 updatetext"


python3 core8/pwb.py fix_mass/fix_sets/new_all get:1 del2 updatetext noapi

tfj run cdcdwww --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/new_all get:1 del2 updatetext noapi"
