#!/usr/bin/python3
"""

إيجاد التحويلات واصلاحها

python3 core8/pwb.py mdpy/fixred

"""
#
# (C) Ibrahem Qasim, 2022
#
#
# ---
import re
import sys
from apis import mdwiki_api
from newapi import printe
from mdpy.bots import py_tools
from newapi.mdwiki_page import MainPage as md_MainPage, NEW_API

NewList = {}

redirects_pages = mdwiki_api.Get_All_pages("!", namespace="0", apfilterredir="redirects")
print(f"len of redirects_pages {len(redirects_pages)} ")
# ---
nonredirects = mdwiki_api.Get_All_pages("!", namespace="0", apfilterredir="nonredirects")

printe.output(f"len of nonredirects {len(nonredirects)} ")

from_to = {}
normalized = {}
# ---


def printtest(s):
    if "test" in sys.argv:
        print(s)


def find_redirects(links):
    # ---
    # titles = [ x for x in links if links[x].get('ns','') == '0' ]
    titles = []
    for x in links:
        if x not in from_to:
            ns = links[x].get("ns", "")
            if str(ns) == "0":
                titles.append(x)
            else:
                printe.output(f"ns:{str(ns)}")
    # ---
    oldlen = len(from_to.items())
    # ---
    normalized_numb = 0
    # ---
    for i in range(0, len(titles), 300):
        group = titles[i : i + 300]
        # ---
        # printe.output(group)
        # ---
        line = "|".join(group)
        # ---
        params = {
            "action": "query",
            "format": "json",
            "prop": "redirects",
            "titles": line,
            "redirects": 1,
            "converttitles": 1,
            "utf8": 1,
            "rdlimit": "max",
        }
        if jsone := mdwiki_api.post_s(params):
            # ---
            query = jsone.get("query", {})
            # ---
            # "normalized": [{"from": "tetracyclines","to": "Tetracyclines"}]
            normal = query.get("normalized", [])
            for nor in normal:
                normalized[nor["to"]] = nor["from"]
                normalized_numb += 1
                # printe.output('normalized["%s"] = "%s"' % ( nor["to"] , nor["from"] ) )
            # ---
            # "redirects": [{"from": "Acetylsalicylic acid","to": "Aspirin"}]
            Redirects = query.get("redirects", [])
            for red in Redirects:
                from_to[red["from"]] = red["to"]
                # printe.output('from_to["%s"] = "%s"' % ( red["from"] , red["to"] ) )
            # ---
            # "pages": { "4195": {"pageid": 4195,"ns": 0,"title": "Aspirin","redirects": [{"pageid": 4953,"ns": 0,"title": "Acetylsalicylic acid"}]} }
            pages = query.get("pages", {})
            # ---
            for page in pages:
                # tab = {"pageid": 4195,"ns": 0,"title": "Aspirin","redirects": [{"pageid": 4953,"ns": 0,"title": "Acetylsalicylic acid"}]}
                tab = pages[page]
                for pa in tab.get("redirects", []):
                    from_to[pa["title"]] = tab["title"]
                    # printe.output('<<lightyellow>> from_to["%s"] = "%s"' % ( pa["title"] , tab["title"] ) )
        else:
            printe.output(" no jsone")
    # ---
    newlen = len(from_to.items())
    nn = newlen - oldlen
    # ---
    printe.output(f"def find_redirects: find {nn} length")
    # printe.output( "def find_redirects: find %d for normalized" % normalized_numb )


def replace_links2(text, oldlink, newlink):
    # ---
    oldlink2 = normalized.get(oldlink, oldlink)
    # ---
    while text.find(f"[[{oldlink}]]") != -1 or text.find(f"[[{oldlink}|") != -1 or text.find(f"[[{oldlink2}]]") != -1 or text.find(f"[[{oldlink2}|") != -1:
        # ---
        printe.output(f"text.replace( '[[{oldlink}]]' , '[[{newlink}|{oldlink}]]' )")
        # ---
        text = text.replace(f"[[{oldlink}]]", f"[[{newlink}|{oldlink}]]")
        text = text.replace(f"[[{oldlink}|", f"[[{newlink}|")
        # ---
        text = re.sub(r"\[\[%s(\|\]\])" % oldlink, r"[[%s\g<1>" % newlink, text, flags=re.IGNORECASE)
        # ---
        if oldlink != oldlink2:
            text = re.sub(r"\[\[%s(\|\]\])" % oldlink2, r"[[%s\g<1>" % newlink, text, flags=re.IGNORECASE)
            text = text.replace(f"[[{oldlink2}]]", f"[[{newlink}|{oldlink2}]]")
            text = text.replace(f"[[{oldlink2}|", f"[[{newlink}|")
    # ---
    return text


def treat_page(title):
    """
    Change all redirects from the current page to actual links.
    """
    # ---
    page = md_MainPage(title, "www", family="mdwiki")
    exists = page.exists()
    # ---
    text = page.get_text()
    # ---
    # links = page.page_links_query(plnamespace="0")
    links = mdwiki_api.Get_page_links(title, namespace="0", limit="max")
    # ---
    normal = links.get("normalized", [])
    printe.output(f"find {len(normal)} normalized..")
    # ---
    for nor in normal:
        normalized[nor["to"]] = nor["from"]
        printe.output(f"normalized[\"{nor['to']}\"] = \"{nor['from']}\"")
    # ---
    newtext = text
    # ---
    find_redirects(links["links"])
    # ---
    for tt in links["links"]:
        # ---
        page = links["links"][tt]
        tit = page["title"]
        tit2 = normalized.get(page["title"], page["title"])
        # ---
        if fixed_tit := from_to.get(tit) or from_to.get(tit2):
            newtext = replace_links2(newtext, tit, fixed_tit)
        elif tit not in nonredirects:
            if tit2 != tit:
                printe.output(f'<<lightred>> tit:["{tit}"] and tit:["{tit2}"] not in from_to')
    # ---
    save_page = page.save(newtext=newtext, summary="Fix redirects")


def main():
    # ---
    ttab = []
    # ---
    # python3 fixred.py
    # python  fixred.py test -page:WikiProjectMed:List ask
    # python  fixred.py test -page:User:Mr._Ibrahem/sandbox
    # python3 fixred.py test -page:Tetracycline_antibiotics
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        # ---
        if arg in ["-page2", "page2"]:
            value = py_tools.ec_de_code(value.strip(), "decode")
            ttab.append(value.strip())
        # ---
        if arg == "-page":
            ttab.append(value)
    # ---
    if ttab in [[], ["all"]]:
        ttab = nonredirects
    # ---
    for title in ttab:
        treat_page(title)

    # ---


# ---
if __name__ == "__main__":
    main()
# ---
