#!/usr/bin/python3
"""

"""
#
# (C) Ibrahem Qasim, 2023
#
#
import codecs
import sys
# ---
from new_api.mdwiki_page import MainPage, NEW_API
# ---
from pathlib import Path
Dir = str(Path(__file__).parents[0])
#print(f'Dir : {Dir}')
# ---
dir2 = Dir.replace('\\', '/')
dir2 = dir2.split('/mdwiki/')[0] + '/mdwiki'
# ---
public_html = dir2 + '/public_html'
# ---
api_new = NEW_API('www', family='mdwiki')
api_new.Login_to_wiki()
# pages   = api_new.Find_pages_exists_or_not(liste)
# pages   = api_new.Get_All_pages(start='', namespace="0", limit="max", apfilterredir='', limit_all=0)
# ---
file_name = {}
numbers = {1: 20000, 'done': 0}


def work(title, Find, Replace, nn):
    # ---
    page = MainPage(title, 'www', family='mdwiki')
    exists = page.exists()
    if not exists:
        return
    # ---
    # if page.isRedirect() :  return
    # target = page.get_redirect_target()
    # ---
    text = page.get_text()
    # ---
    if text.strip() == '':
        print(f"page:{title} text = ''")
        line = '"%s":"no changes",\n' % title.replace('"', '\\"')
        with codecs.open(file_name[1], 'a', encoding="utf-8") as file:
            file.write(line)
        return
    # ---
    new_text = text
    # ---
    if 'testtest' in sys.argv:
        new_text = new_text.replace(Find, Replace, 1)
    else:
        new_text = new_text.replace(Find, Replace)
    # ---
    if new_text == text:
        line = '"%s":"no changes",\n' % title.replace('"', '\\"')
        with codecs.open(file_name[1], 'a', encoding="utf-8") as file:
            file.write(line)
        return
    # ---
    numbers['done'] += 1
    # ---
    revid = page.revid
    # ---
    sus = f'replace {nn} [[toolforge:mdwiki/qdel.php?job=replace{nn}|(stop)]] '
    # ---
    save_page = page.save(newtext=new_text, summary=sus)
    # ---
    line = '"%s":%d,\n' % (title.replace('"', '\\"'), 0)
    # ---
    if save_page:
        # ---
        newrevid = page.newrevid
        # ---
        if newrevid != revid and newrevid != '':
            # ---
            line = '"%s":%d,\n' % (title.replace('"', '\\"'), newrevid)
            # ---
    # ---
    with codecs.open(file_name[1], 'a', encoding="utf-8") as file:
        file.write(line)


def main():
    # pywikibot.output( '*<<lightred>> > main:')
    # ---
    nn = ''
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        # ---
        if arg == "-rand":
            nn = value
        # ---
        if arg == "-number" and value.isdigit():
            # if re.match(r'^(\d|\d+)$' , value.strip() ) :
            numbers[1] = int(value)
    # ---
    print(nn)
    # ---
    find = codecs.open(public_html + f'/find/{nn}_find.txt', 'r', 'utf8').read()
    # ---
    replace = codecs.open(public_html + f'/find/{nn}_replace.txt', 'r', 'utf8').read()
    # ---
    if replace.strip() == "empty":
        replace = ""
    # ---
    if 'testtest' in sys.argv:
        find = ','
        replace = ', '
        nn = 0
    # ---
    file_name[1] = public_html + f'/find/log/{nn}.txt'
    # ---
    with codecs.open(Path(file_name[1]), 'w', encoding="utf-8") as file:
        file.write('')
    # ---
    file_name[2] = public_html + f'/find/log/{nn}-text.txt'
    # ---
    if 'newlist' in sys.argv:
        Add_pa = {"srsort": "just_match", "srwhat": "text"}
        # ---
        titles = api_new.Search(value=find, ns="0", srlimit="max", RETURN_dict=False, addparams=Add_pa)
    else:
        titles = api_new.Get_All_pages()
        # ---
    # ---
    text = f"start work in {len(titles)} pages."
    line = "<span style='font-size:12px'>" + text + "</span>"
    codecs.open(file_name[2], 'w', encoding="utf-8").write(line)
    # ---
    num = 0
    # ---
    for page in titles:
        num += 1
        # ---
        if numbers['done'] >= numbers[1]:
            break
        # ---
        work(page, find, replace, nn)

    # ---


# python py/replace1.py
# ---
if __name__ == "__main__":
    main()
# ---
