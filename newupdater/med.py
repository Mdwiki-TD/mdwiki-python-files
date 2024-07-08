#!/usr/bin/python3
"""
python3 I:/mdwiki/pybot/newupdater/med.py Aspirin from_toolforge
"""
import sys
from pathlib import Path

Dir = str(Path(__file__).parents[0])
dir2 = Dir.replace("\\", "/").split("/pybot/")[0]

dir3 = dir2 + "/pybot"
sys.path.append(dir3)
# --
from newupdater.helps import ec_de_code
from newupdater.MedWorkNew import work_on_text
from newupdater.mdapi import GetPageText2, GetPageText, page_put


def get_new_text(title):
    # ---
    text = GetPageText2(title)
    # ---
    if not text:
        text = GetPageText(title)
    # ---
    newtext = text
    # ---
    if newtext != "":
        newtext = work_on_text(title, newtext)
    # ---
    return text, newtext


def work_on_title(title):
    # ---
    title = ec_de_code(title, "decode")
    # ---
    text, new_text = get_new_text(title)
    # ---
    if text.strip() == "" or new_text.strip() == "":
        print("notext")
        return
    elif text == new_text:
        print("no changes")
        return
    elif not new_text:
        print("notext")
        return
    elif "save" in sys.argv:
        return page_put(text, new_text, "", title, "")
    # ---
    title2 = title.replace(" ", "_")
    title2 = title2.replace(":", "-").replace("/", "-")
    # ---
    try:
        filename = f"{dir2}/public_html/updatercash/{title2}_1.txt"
        # ---
        open(filename, "w", encoding="utf-8").write(new_text)
        # ---
        print(filename)
        # ---
    except Exception:
        filename = f"{dir2}/public_html/updatercash/title2.txt"
        # ---
        open(filename, "w", encoding="utf-8").write(new_text)
        # ---
        print(filename)


def main():
    # ---
    title = ""
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        arg = arg[1:] if arg.startswith("-") else arg
        # ---
        if arg == "page":
            title = value.replace("_", " ")
    # ---
    if title == "":
        print("no page")
        return
    # ---
    work_on_title(title)


if __name__ == "__main__":
    main()
