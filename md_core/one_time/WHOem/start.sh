#!/bin/bash

# get all langlinks
python3 core8/pwb.py WHOem/bot

python3 core8/pwb.py WHOem/find_views_by_lang new

python3 core8/pwb.py WHOem/make_text ask

cp md_core/WHOem/lists/views.json public_html/WHO/Tables/views.json