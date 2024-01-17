#!/usr/bin/python3
"""

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import sys
import urllib.parse
from pathlib import Path

# ---
Dir = Path(__file__).parent.parent
# ---
sys.path.append(str(Dir))
# ---
from TDpynew import printe
from TDpynew import text_changes
from TDpynew import ref
from TDpynew import mdapi
from TDpynew import enapi

# ---
wholearticle = {1: False}
# ---
Url_To_login = {1: '', 'not': True}
# ---
login_done = {1: False}


def print_py(s):
    if sys.stdin.isatty():
        print(s)


def put(title, text):
    # ---
    suus = 'from https://mdwiki.org/wiki/' + title.replace(' ', '_')
    # ---
    title2 = f'User:Mr. Ibrahem/{title}'
    if wholearticle[1]:
        title2 = f'User:Mr. Ibrahem/{title}/full'

    # ---
    dataa = {
        "format": "json",
        "utf8": 1,
        "action": "edit",
        "title": title2,
        "text": text,
        "summary": suus,
        # "nocreate": 1,
    }
    # ---
    js = enapi.submitAPI(dataa, addtoken=True)
    # ---
    if 'Success' in str(js):
        print('true')
    else:
        print(js)


def work(title):
    # ---
    title = urllib.parse.unquote(title)
    # ---
    print_py(f'title:{title}')
    # ---
    if 'test' in sys.argv:
        print(title)
    # ---
    params2 = {"action": "parse", "format": "json", "page": title, "prop": "wikitext"}
    # ---
    json2 = mdapi.submitAPI(params2)
    # ---
    alltext = json2.get("parse", {}).get("wikitext", {}).get("*", '')
    # ---
    first = ''
    # ---
    if wholearticle[1]:
        first = alltext
    else:
        params = {"action": "parse", "format": "json", "page": title, "prop": "wikitext", "section": "0"}
        json1 = mdapi.submitAPI(params)
        first = json1.get("parse", {}).get("wikitext", {}).get("*", '')
    # ---
    text = first
    # ---
    if text == '':
        print_py('no text')
        return "notext"
    # ---
    if not wholearticle[1]:
        # text += '\n==References==\n<references />\n[[en:%s]]' % title
        text += '\n==References==\n<references />'
    # ---
    newtext = ref.fix_ref(text, alltext)
    # ---
    newtext = text_changes.work(newtext)
    # ---
    newtext = newtext.replace('[[Category:', '[[:Category:')
    # ---
    if newtext == '':
        print_py('no text')
        return "notext"
    # ---
    if 'ask' in sys.argv:
        printe.showDiff(text, newtext)
        ask = input('save?')
        if ask not in ['y', 'Y', '']:
            return
    # ---
    return put(title, newtext)


if __name__ == '__main__':
    title = ''
    # ---
    # python3 I:/mdwiki/pybot/TDpynew/translate.py -title:Endometrial_cancer
    # python3 core8/pwb.py TDpynew/translate -title:Endometrial_cancer
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        # ---
        if arg == "-title":
            title = value
        elif arg == "wholearticle":
            wholearticle[1] = True
    # ---
    if title != '':
        work(title)
