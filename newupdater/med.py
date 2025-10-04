#!/usr/bin/python3
"""
python3 I:/mdwiki/pybot/newupdater/med.py -page:Aspirin from_toolforge
"""
import os
import sys

home_dir = os.getenv("HOME") or "I:/mdwiki/mdwiki"

sys.path.append(home_dir + "/pybot")
sys.path.append(home_dir + "/openssl/bin")
# --
public_html_dir = home_dir + "/public_html"
# --
from new_updater import ec_de_code, work_on_text
from mdapi import GetPageText, page_put, login


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
    filename = f"{public_html_dir}/updatercash/{title2}_1.txt"
    # ---
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(new_text)
    except Exception:
        filename = f"{public_html_dir}/updatercash/title2.txt"
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
        # ---
        if arg in ["-page", "page"]:
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
