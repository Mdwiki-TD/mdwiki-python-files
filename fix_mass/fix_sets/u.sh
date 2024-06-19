#!/bin/bash
# fix cases
python3 core8/pwb.py mass/radio/st3/o2 del2 nomulti ask

# then fix studies
python3 core8/pwb.py fix_mass/fix_sets/o
