"""

python3 core8/pwb.py WHOem/make_text

"""

import sys
import codecs
import json
from pathlib import Path

# ---
from WHOem import sections_text
from new_api.mdwiki_page import MainPage as md_MainPage

# ---
Dir = Path(__file__).parent
# ---
with codecs.open(f'{Dir}/lists/views.json', 'r', 'utf-8') as f:
    ViewsData = json.load(f)
# ---
print(f'len ViewsData: {len(ViewsData)}')
# ---
ntext = sections_text.make_text(ViewsData)
# ---
if 'test' in sys.argv:
    print(ntext)
# ---
with codecs.open(f'{Dir}/text.txt', 'w', 'utf-8') as f:
    f.write(ntext)
# ---
title = 'User:Mr. Ibrahem/WHOem'
# ---
page = md_MainPage(title, 'www', family='mdwiki')
if exists := page.exists():
    # ---
    text = page.get_text()
    save_page = page.save(newtext=ntext, summary='update', nocreate=1, minor='')
else:
    create = page.Create(text=ntext, summary='update')
