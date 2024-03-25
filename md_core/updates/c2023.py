#!/usr/bin/python3
"""

python3 core8/pwb.py updates/c2023
python3 core8/pwb.py updates/c2023 prior

tfj run c202c --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py updates/c2023"

"""
#
# (C) Ibrahem Qasim, 2022
#
#

import json
import sys
from pathlib import Path
import wikitextparser as wtp
from mdpy.bots import mdwiki_api
# ---
Dir = Path(__file__).parent
# ---
from newapi.mdwiki_page import NEW_API, MainPage as md_MainPage
api_new = NEW_API('www', family='mdwiki')
# login    = api_new.Login_to_wiki()
# ---
limit = 200 if 'test' in sys.argv else 100000
# ---


def get_users(pages):
    usersbyyear = {'all': {}, '2023': {}, '2022': {}, '2021': {}}
    # ---
    for num, title in enumerate(pages, start=1):
        # ---
        print(f'num:{num}/{len(pages)}, title:{title}')
        # ---
        revisions= api_new.get_revisions(title, rvprop='user|timestamp|comment', options={"rvstart": "2021-01-01T00:00:00.000Z", "rvend": "2024-01-01T00:00:00.000Z"})
        # ---
        for ref in revisions:
            refs = ref.get("revisions", [])
            for r in refs:
                timestamp = r.get("timestamp", '')
                # ---
                if r.get('anon'):
                    continue
                # ---
                # if not timestamp.startswith('2023'): continue
                # ---
                user = r.get("user", '')
                comment = r.get("comment", '')
                # ---
                if comment.startswith('Reverted edits'):
                    continue
                # ---
                if user.lower().endswith('bot'):
                    continue
                # ---
                year = timestamp[:4]
                if year not in usersbyyear:
                    usersbyyear[year] = {}
                # ---
                # print(f'user:{user}, comment:{comment}')
                # ---
                if user == 'Mr. Ibrahem':
                    # if comment == 'mdwiki changes.' or comment.startswith('add link to'):
                    continue
                # ---
                usersbyyear['all'][user] = usersbyyear['all'].get(user, 0) + 1
                usersbyyear[year][user] = usersbyyear[year].get(user, 0) + 1
    # ---
    return usersbyyear


# ---
title = 'User:Mr. Ibrahem/stats'
# ---
if 'prior' in sys.argv:
    title = 'User:Mr. Ibrahem/2023/prior'

    page = md_MainPage("WikiProjectMed:List/Prior", 'www', family='mdwiki')

    text = page.get_text()
    # Parse the text content of the page using wikitextparser
    parser = wtp.parse(text)

    # Get the top-level sections of the parsed page
    wikilinks = parser.wikilinks
    pages = [str(x.title) for x in wikilinks]
    pages = list(set(pages))
else:
    pages = mdwiki_api.Get_All_pages('!', namespace='0', limit=limit, limit_all=limit, apfilterredir='nonredirects')
# ---
usersbyyear = get_users(pages)
# ---
text = f'* pages: {len(pages):,}'
# ---
# sort usersbyyear keys
# usersbyyear = dict(sorted(usersbyyear.items()))
# ---
for year, usersx in usersbyyear.items():
    text += (
        f'\n== {year} stats ==\n'
        '{| class="wikitable sortable"\n'
        '|-\n! #\n! user\n! count\n'
    )
    # ---
    sorted_users = sorted(usersx.items(), key=lambda x: x[1], reverse=True)
    # ---
    numb = 0
    # ---
    for num, (user, count) in enumerate(sorted_users, 1):
        text += f'|-\n| {num}\n| [[User:{user}|{user}]]\n| {count:,}\n'
    # ---
    text += '''|-
    |}
    '''
# ---
page = md_MainPage(title, 'www', family='mdwiki')
# ---
if not page.exists():
    page.Create(text=text, summary='update')
else:
    page.save(newtext=text, summary='update')
# ---
