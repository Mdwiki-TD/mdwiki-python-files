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
if "dir3" in sys.argv:
    print("dir3: ", dir3)
# --
from newupdater.helps import ec_de_code
from newupdater.MedWorkNew import work_on_text
from newupdater.mdapi import GetPageText, page_put, login


def get_new_text(title):
    # ---
    # if not text:
    text = GetPageText(title)
    # ---
    newtext = text
    # ---
    if newtext != "":
        newtext = work_on_text(title, newtext)
    # ---
    return text, newtext


def save_cash(title, new_text):
    # ---
    title2 = title
    title2 = title2.replace(":", "-").replace("/", "-").replace(" ", "_")
    # ---
    filename = f"{dir2}/public_html/updatercash/{title2}_1.txt"
    # ---
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(new_text)
    except Exception:
        filename = f"{dir2}/public_html/updatercash/title2.txt"
        # ---
        with open(filename, "w", encoding="utf-8") as f:
            f.write(new_text)
    # ---
    return filename


def work_on_title(title):
    # ---
    title = ec_de_code(title, "decode")
    # ---
    text, new_text = get_new_text(title)
    # ---
    if text.strip() == "" or new_text.strip() == "":
        print("notext")
        return
    # ---
    if text == new_text:
        print("no changes")
        return
    # ---
    if not new_text:
        print("notext")
        return
    # ---
    if "save" in sys.argv:
        a = page_put(text, new_text, "Med updater.", title, "")
        if a:
            print("save ok")
            return ""
    # ---
    filee = save_cash(title, new_text)
    # ---
    print(filee)
    # ---
    return ""


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
        return ""
    # ---
    login("")
    # ---
    work_on_title(title)
    # ---
    return ""


if __name__ == "__main__":
    main()
