#!/usr/bin/python3
"""

إنشاء تحويلات من العنوان الإنجليزي
إلى العنوان المحلي
في orwiki

python3 core8/pwb.py mdpy/orred

"""
from mdpy.bots import sql_for_mdwiki
from mdpy.bots import wiki_api
from newapi import printe

# wiki_api.Get_page_qids(sitecode, titles)
# wiki_api.submitAPI( params, apiurl = 'https://' + 'www.wikidata.org/w/api.php', returnjson = False )
# wiki_api.submitAPI_token( params, apiurl = 'https://' + 'www.wikidata.org/w/api.php', returnjson = False )
# wiki_api.Find_pages_exists_or_not( liste, apiurl = 'https://' + 'or.wikipedia.org/w/api.php' )
# wiki_api.Getpageassessments_from_wikipedia( titles, site="en", find_redirects=False, pasubprojects=0 )
# wiki_api.get_page_views(titles, site='en', days = 30)
# wiki_api.get_views_with_rest_v1(langcode, titles, date_start='20040101', date_end='20300101', printurl=False, printstr=False)
# wiki_api.GetPageText(title, lang, redirects=False)
# wiki_api.get_langlinks(title, lang)
# ---
or_url = f"https://or.wikipedia.org/w/api.php"


def create_redirect(target, mdtitle):
    # ---
    exists = wiki_api.Find_pages_exists_or_not([target, mdtitle], apiurl=or_url)
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
        text = f"#redirect [[{target}]]"
        sus = f"Redirected page to [[{target}]]"
        params = {
            "action": "edit",
            "format": "json",
            "title": mdtitle,
            "text": text,
            "summary": sus,
            "createonly": 1,
            "utf8": 1,
            "token": "",
        }
        # ---
        uu = wiki_api.submitAPI_token(params, apiurl="https://" + "www.wikidata.org/w/api.php", returnjson=False)
        # ---
        if "Success" in uu:
            printe.output(f"<<lightgreen>>** true .. [[{mdtitle}]] ")
        else:
            printe.output(uu)


def dodo_sql():
    # ---
    que = """select title, target from pages where target != "" and lang = "or";"""
    # ---
    sq = sql_for_mdwiki.mdwiki_sql(que, return_dict=True)
    # ---
    for n, tab in enumerate(sq, start=1):
        mdtitle = tab["title"]
        target = tab["target"]
        # ---
        printe.output(f'----------\n*<<lightyellow>> p{n}/{len(sq)} >target:"{target}".')
        # ---
        create_redirect(target, mdtitle)


if __name__ == "__main__":
    dodo_sql()
