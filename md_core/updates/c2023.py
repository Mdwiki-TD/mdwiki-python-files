#!/usr/bin/python3
"""

python3 core8/pwb.py updates/c2023 

"""
#
# (C) Ibrahem Qasim, 2022
#
#

from mdpy.bots import mdwiki_api
import sys
from pathlib import Path
import codecs
# ---
Dir = Path(__file__).parent
# ---
users = {}
# ---
from new_api.mdwiki_page import NEW_API
api_new  = NEW_API('www', family='mdwiki')
# login    = api_new.Login_to_wiki()

pages = mdwiki_api.Get_All_pages('!', namespace='0', limit=10, limit_all=10, apfilterredir='nonredirects')
# ---
for title in pages:
    # ---
    revisions= api_new.get_revisions(title, rvprop='user|timestamp', options={"rvstart": "2023-01-01T00:00:00.000Z", "rvend": "2024-01-23T18:23:33.000Z"})
    # ---
    for ref in revisions:
        user = ref.get("user", '')
        print(f'user:{user}')
        users[user] = users.get(user, 0) + 1
# ---
sorted_users = sorted(users.items(), key=lambda x: x[1], reverse=True)
# ---
print(f'has {len(sorted_users)} sorted_users. ')
# ---
text = '''
--~~~~
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
#---
'''
if 'test' in sys.argv:
    print(text)
else:
    mdwiki_api.page_put(newtext=text, summary='update', title='User:Mr. Ibrahem/2023')
# ---