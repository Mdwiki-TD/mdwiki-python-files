#!/usr/bin/python3
"""

إنشاء تحويلات من العنوان الإنجليزي
إلى العنوان المحلي
في orwiki

python3 core8/pwb.py mdpy/orred

"""
#
# (C) Ibrahem Qasim, 2022
#
#

# ---

# ---
# ---
from mdpy.bots import sql_for_mdwiki

# sql_for_mdwiki.mdwiki_sql(query , update = False)
# ---
from mdpy import printe
from mdpy import wpref
from wprefs.api import submitAPI  # (params, lang='', Type='post')

# ---
or_url = 'https://' + 'or.wikipedia.org/w/api.php'


def Find_pages_exists_or_not(liste, apiurl=''):
    # ---
    params = {
        "action": "query",
        "format": "json",
        "titles": '|'.join(liste),
        # "redirects": 0,
        # "prop": "templates|langlinks",
        "utf8": 1,
        "token": "",
    }
    # ---
    table = {}
    # ---
    json1 = submitAPI(params, lang='or')
    # ---
    if json1:
        query_pages = json1.get("query", {}).get("pages", {})
        for page in query_pages:
            kk = query_pages[page]
            if "title" in kk:
                tit = kk.get("title", "")
                # ---
                table[tit] = "missing" not in kk
    return table


def create_redirect(target, mdtitle):
    # ---
    exists = Find_pages_exists_or_not([target, mdtitle], apiurl=or_url)
    # ---
    Worrk = False
    # ---
    for tit, o in exists.items():
        if o is False:
            if tit.lower() == target.lower():
                printe.output(f" target:{target} not exists in orwiki.")
                return ""
            elif tit.lower() == mdtitle.lower():
                Worrk = True
    # ---
    if Worrk:
        # ---
        text = f'#redirect [[{target}]]'
        sus = f'Redirected page to [[{target}]]'
        params = {"action": "edit", "format": "json", "title": mdtitle, "text": text, "summary": sus, "createonly": 1, "utf8": 1, "token": ""}
        # ---
        uu = submitAPI(params, lang='or')
        # ---
        if 'Success' in uu:
            printe.output(f'<<lightgreen>>** true .. [[{mdtitle}]] ')
        else:
            printe.output(uu)


def dodo_sql():
    # ---
    que = '''select title, target from pages where target != "" and lang = "or";'''
    # ---
    sq = sql_for_mdwiki.mdwiki_sql(que, return_dict=True)
    # ---
    for n, tab in enumerate(sq, start=1):
        mdtitle = tab['title']
        target = tab['target']
        # ---
        printe.output(f'----------\n*<<lightyellow>> p{n}/{len(sq)} >target:"{target}".')
        # ---
        create_redirect(target, mdtitle)


if __name__ == "__main__":
    dodo_sql()
