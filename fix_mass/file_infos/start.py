"""

tfj run --mem 2Gi startx --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/file_infos/start"


python3 core8/pwb.py fix_mass/file_infos/start debug
python3 core8/pwb.py fix_mass/file_infos/start

Category:Radiopaedia case Active rickets id: 58738 study: 65957

"""
import os
import sys
import psutil
import re

# from pathlib import Path
# from newapi import printe
from fix_mass.file_infos.p2 import get_files
from fix_mass.file_infos.db import insert_all_infos  # insert_all_infos(data_list, prnt=True)

debug = "debug" in sys.argv
number = 10 if debug and "no" not in sys.argv else 2000

add_to_db_done = 0


def print_memory():
    yellow, purple = "\033[93m%s\033[00m", "\033[95m%s\033[00m"

    usage = psutil.Process(os.getpid()).memory_info().rss
    usage = usage / 1024 // 1024

    print(yellow % "Memory usage:", purple % f"{usage} MB")


def add_to_db(data_list, prnt=True):
    # ---
    global add_to_db_done
    # ---
    add_to_db_done += len(data_list)
    # ---
    print(f"add_to_db ({add_to_db_done}): len: {len(data_list)}")
    # ---
    if debug:
        del data_list
        return
    # ---
    return insert_all_infos(data_list, prnt=prnt)


def get_img_url_from_content(content):
    # find urls
    urls = re.findall(r"(?P<url>https?://[^\s]+)", content)
    # ---
    for url in urls:
        if "prod-images-static.radiopaedia.org" in url:
            return url
    # ---
    return ""


def match_id(content):
    # ---
    # match * Image ID: 10422592
    ma = re.findall(r"Image ID: (\d+)", content)
    img_id = ""
    if ma:
        img_id = ma[0]
    # ---
    return img_id


def one_row(tab):
    # ---
    file = tab["title"]
    # ---
    new = {"url": "", "urlid": "", "file": file}
    # ---
    parentid = tab["parentid"]
    # ---
    if parentid == 0:
        # ---
        content = tab["content"]
        url = get_img_url_from_content(content)
        # ---
        if url:
            new["url"] = url
            ma = re.match(r"https://prod-images-static.radiopaedia.org/images/(\d+)/", url)
            if ma:
                new["urlid"] = ma.group(1)
        else:
            new["urlid"] = match_id(content)
    # ---
    return new


def main():
    files = get_files(load_json=True)
    # ---
    to_work = []
    # ---
    for n, tab in enumerate(files):
        # ---
        new = one_row(tab)
        # ---
        to_work.append(new)
        # ---
        if n % number == 0:
            add_to_db(to_work)
            del to_work
            to_work = []
            print_memory()
    # ---
    add_to_db(to_work)


if __name__ == "__main__":
    # ---
    main()
