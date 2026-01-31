#!/usr/bin/python3
""" """
import os
import sys
from pathlib import Path

from mdwiki_api.mdwiki_page import NEW_API, MainPage

# ---
if os.getenv("HOME"):
    dir2 = os.getenv("HOME") + "/public_html"
else:
    dir2 = "I:/mdwiki/mdwiki/public_html"
# ---
work_dir = f"{dir2}/replace/find"
# ---
api_new = NEW_API("www", family="mdwiki")
file_name = {}

numbers = {1: 20000, "done": 0}


def work(title, Find, Replace, nn):
    # ---
    page = MainPage(title, "www", family="mdwiki")
    exists = page.exists()
    if not exists:
        return
    # ---
    # if page.isRedirect() :  return
    # target = page.get_redirect_target()
    # ---
    text = page.get_text()
    # ---
    if not text.strip():
        print(f"page:{title} text = ''")
        line = '"%s":"no changes",\n' % title.replace('"', '\\"')
        with open(file_name[1], "a", encoding="utf-8") as file:
            file.write(line)
        return
    # ---
    new_text = text
    # ---
    if "testtest" in sys.argv:
        new_text = new_text.replace(Find, Replace, 1)
    else:
        new_text = new_text.replace(Find, Replace)
    # ---
    if new_text == text:
        line = '"%s":"no changes",\n' % title.replace('"', '\\"')
        with open(file_name[1], "a", encoding="utf-8") as file:
            file.write(line)
        return
    # ---
    numbers["done"] += 1
    # ---
    revid = page.get_revid()
    # ---
    sus = f"replace {nn} [[toolforge:mdwiki/qdel.php?job=replace{nn}|(stop)]] "
    # ---
    save_page = page.save(newtext=new_text, summary=sus)
    # ---
    line = '"%s":%d,\n' % (title.replace('"', '\\"'), 0)
    # ---
    if save_page:
        # ---
        newrevid = page.get_newrevid()
        # ---
        if newrevid not in [revid, ""]:
            # ---
            line = '"%s":%d,\n' % (title.replace('"', '\\"'), newrevid)
            # ---
    # ---
    with open(file_name[1], "a", encoding="utf-8") as file:
        file.write(line)


def main():
    # ---
    nn = ""
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        # ---
        if arg == "-rand":
            nn = value
        # ---
        if arg == "-number" and value.isdigit():
            numbers[1] = int(value)
    # ---
    print(nn)
    # ---
    find_file = f"{work_dir}/{nn}/find.txt"
    replace_file = f"{work_dir}/{nn}/replace.txt"
    log_file = f"{work_dir}/{nn}/log.txt"
    text_file = f"{work_dir}/{nn}/text.txt"
    # ---
    with open(find_file, "r", encoding="utf-8") as file:
        find = file.read()
    # ---
    with open(replace_file, "r", encoding="utf-8") as file:
        replace = file.read()
    # ---
    if replace.strip() == "empty":
        replace = ""
    # ---
    if "testtest" in sys.argv:
        find = ","
        replace = ", "
        nn = 0
    # ---
    file_name[1] = log_file
    # ---
    with open(Path(file_name[1]), "w", encoding="utf-8") as file:
        file.write("")
    # ---
    file_name[2] = text_file
    # ---
    if "newlist" in sys.argv:
        Add_pa = {"srsort": "just_match", "srwhat": "text"}
        # ---
        titles = api_new.Search(value=find, ns="0", srlimit="max", RETURN_dict=False, addparams=Add_pa)
    else:
        titles = api_new.Get_All_pages()
    # ---
    text = f"start work in {len(titles)} pages."
    line = f"<span style='font-size:12px'>{text}</span>"
    open(file_name[2], "w", encoding="utf-8").write(line)
    # ---
    for _, page in enumerate(titles, start=1):
        # ---
        if numbers["done"] >= numbers[1]:
            break
        # ---
        work(page, find, replace, nn)


if __name__ == "__main__":
    # python py/replace1.py
    main()
