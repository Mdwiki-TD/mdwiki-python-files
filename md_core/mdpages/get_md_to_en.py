#!/usr/bin/python3
"""

(missing_in_enwiki|medwiki_to_enwiki|sames)\.json

Usage:

# python3 core8/pwb.py mdpages/get_md_to_en nodump
# python3 core8/pwb.py mdpages/get_md_to_en other
# python3 core8/pwb.py mdpages/get_md_to_en other nodump

"""
import json
import sys
import os

# ---
from mdpy.bots import catdepth2
from mdpy.bots import wiki_api
from mdpy.bots import mdwiki_api
from mdpy import printe
from mdpy.bots.check_title import valid_title  # valid_title(title)

# ---
from pathlib import Path

Dir = str(Path(__file__).parents[0])
# print(f'Dir : {Dir}')
# ---
dir2 = Dir.replace('\\', '/')
dir2 = dir2.split('/mdwiki/')[0] + '/mdwiki'
# ---
dir2 += '/public_html/Translation_Dashboard/Tables/'
# ---
medwiki_to_enwiki_conflic = {}
medwiki_to_enwiki = {}
missing_in_enwiki = []
sames = []
# ---
json_ext = "_other.json" if 'other' in sys.argv else ".json"


def check():
    # ---
    printe.output('Get cat pages from cat : RTT')
    # ---
    Listo = catdepth2.make_cash_to_cats(return_all_pages=True)
    # ---
    if 'other' in sys.argv:
        Listo_other = mdwiki_api.Get_All_pages('!', namespace='0', apfilterredir='nonredirects')
        listo2 = [x for x in Listo_other if x not in Listo]
        Listo = listo2
    # ---
    printe.output(f'len of cat pages: {len(Listo)}')
    # ---
    Listo = [x for x in Listo if valid_title(x)]
    # ---
    for i in range(0, len(Listo), 100):
        # ---
        newlist = Listo[i: i + 100]
        # ---
        line = "|".join(newlist)
        # ---
        params = {
            "action": "query",
            "format": "json",
            # "prop": "redirects",
            # "rdlimit": "max"
            "titles": line,
            "redirects": 1,
            "converttitles": 1,
            "utf8": 1,
        }
        # ---
        jsone = wiki_api.submitAPI(params, apiurl='https://' + 'en.wikipedia.org/w/api.php', returnjson=False)
        # ---
        if jsone and 'batchcomplete' in jsone:
            # ---
            query = jsone.get("query", {})
            # ---
            # "redirects": [{"from": "Acetylsalicylic acid","to": "Aspirin"}]
            Redirects = query.get("redirects", [])
            for red in Redirects:
                if red["to"] not in Listo:
                    medwiki_to_enwiki[red["from"]] = red["to"]
                else:
                    medwiki_to_enwiki_conflic[red["from"]] = red["to"]
            # ---
            # "pages": { "4195": {"pageid": 4195,"ns": 0,"title": "Aspirin","redirects": [{"pageid": 4953,"ns": 0,"title": "Acetylsalicylic acid"}]} }
            pages = query.get("pages", {})
            # ---
            # { "-1": { "ns": 0, "title": "Fsdfdsf", "missing": "" }, "2767": { "pageid": 2767, "ns": 0, "title": "ACE inhibitor" } }
            # ---
            for page in pages:
                # ---
                tab = pages[page]
                title = tab['title']
                # ---
                if 'missing' in tab:
                    missing_in_enwiki.append(title)
                else:
                    # printe.output('<<lightyellow>> title["%s"] sames' % title )
                    sames.append(title)
            # ---
        else:
            printe.output("<<lightred>> check.py no jsone")
            printe.output(jsone)
        # ---
    for numb, (fromm, to) in enumerate(medwiki_to_enwiki.items(), start=1):
        faf = f'["{fromm}"]'
        printe.output(f'en titles {numb} from_to{faf.ljust(30)} = "{to}"')
    for numb, mis in enumerate(missing_in_enwiki, start=1):
        printe.output(f'<<lightyellow>> {numb} title:{mis.ljust(25)} missing_in_enwiki')
    # ---
    printe.output('<<lightred>> pages both in mdwiki cat:::')
    for numb, (md, en) in enumerate(medwiki_to_enwiki_conflic.items(), start=1):
        faf = f'["{md}"]'
        fen = f'["{en}"]'
        printe.output(f'<<lightred>> {numb} page{faf.ljust(40)} to enwiki{fen}')
    # ---
    printe.output(f'<<lightgreen>> len of medwiki_to_enwiki:{len(medwiki_to_enwiki)}')
    printe.output(f'<<lightgreen>> len of missing_in_enwiki:{len(missing_in_enwiki)}')
    printe.output(f'<<lightgreen>> len of medwiki_to_enwiki_conflic:{len(medwiki_to_enwiki_conflic)}')
    printe.output(f'<<lightgreen>> len of sames:{len(sames)}')
    # ---
    if 'nodump' not in sys.argv:
        # الكتابة إلى الملفات
        with open(f'{dir2}medwiki_to_enwiki{json_ext}', 'w', encoding='utf-8') as aa:
            json.dump(medwiki_to_enwiki, aa)
        # ---
        with open(f'{dir2}missing_in_enwiki{json_ext}', 'w', encoding='utf-8') as bb:
            json.dump(missing_in_enwiki, bb)
        # ---
        with open(f'{dir2}sames{json_ext}', 'w', encoding='utf-8') as cc:
            json.dump(sames, cc)


if __name__ == '__main__':
    check()
