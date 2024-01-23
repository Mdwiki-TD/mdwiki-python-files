#!/usr/bin/python3
"""

python3 core8/pwb.py updates/c2023 

"""
#
# (C) Ibrahem Qasim, 2022
#
#

import json
import sys
from pathlib import Path
import codecs
from mdpy.bots import mdwiki_api
# ---
Dir = Path(__file__).parent
# ---
users = {}
# ---
from new_api.mdwiki_page import NEW_API, MainPage as md_MainPage
api_new  = NEW_API('www', family='mdwiki')
# login    = api_new.Login_to_wiki()
# ---
limit = 500 if 'test' in sys.argv else 100000
# ---
pages = mdwiki_api.Get_All_pages('!', namespace='0', limit=limit, limit_all=limit, apfilterredir='nonredirects')
# ---
for num, title in enumerate(pages, start=1):
    # ---
    print(f'num:{num}/{len(pages)}, title:{title}')
    # ---
    revisions= api_new.get_revisions(title, rvprop='user|timestamp|comment', options={"rvstart": "2023-01-01T00:00:00.000Z", "rvend": "2024-01-23T18:23:33.000Z"})
    # ---
    for ref in revisions:
        refs = ref.get("revisions", [])
        for r in refs:
            timestamp = r.get("timestamp", '')
            # ---
            if r.get('anon'):
                continue
            # ---
            if not timestamp.startswith('2023'):
                continue
            # ---
            user = r.get("user", '')
            comment = r.get("comment", '')
            # ---
            if comment.startswith('Reverted edits'):
                continue
            # ---
            # print(f'user:{user}, comment:{comment}')
            # ---
            if user == 'Mr. Ibrahem':
                # if comment == 'mdwiki changes.' or comment.startswith('add link to'):
                continue
            # ---
            users[user] = users.get(user, 0) + 1
# ---
sorted_users = sorted(users.items(), key=lambda x: x[1], reverse=True)
# ---
print(f'has {len(sorted_users)} sorted_users. ')
# ---
# dump users
with codecs.open(Dir / 'users.json', 'w', 'utf-8') as f:
    json.dump(users, f, indent=4)
# ---
text = f'* pages: {len(pages):,}'
# ---
text += '''
== 2023 stats ==
{| class="wikitable sortable"
|-
! #
! user
! count
'''
# ---
numb = 0
#---
for num, (user, count) in enumerate(sorted_users, 1):
    text += f'|-\n| {num}\n| [[User:{user}|{user}]]\n| {count:,}\n'
#---
text += '''|-
|}
'''
# ---
page      = md_MainPage('User:Mr. Ibrahem/2023', 'www', family='mdwiki')
# ---
if not page.exists():
    page.Create(text=text, summary='update')
else:
    page.save(newtext=text, summary='update')
# ---
