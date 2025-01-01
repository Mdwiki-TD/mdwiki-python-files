"""

python3 core8/pwb.py stats/o

"""
import json
import re
import os
import sys
from pathlib import Path
from datetime import datetime

# ---
from newapi import printe
from newapi.mdwiki_page import MainPage as md_MainPage
from stats.editors import get_editors, validate_ip

last_year = datetime.now().year - 1
# ---
Dir = Path(__file__).parent
sites_dir = Dir / "sites"
editors_dir = Dir / "editors"
# ---
skip_sites = ["enwiki", "wikidatawiki", "commonswiki", "specieswiki"]


def filter_editors(editors, site):
    # ---
    editors = dict(sorted(editors.items(), key=lambda x: x[1], reverse=True))
    # ---
    for x, v in editors.copy().items():
        if validate_ip(x):
            del editors[x]
    # ---
    # del editor with less then 100 edits
    for x, v in editors.copy().items():
        if v < 10:
            del editors[x]
    # ---
    # del Mr. Ibrahem if site != 'arwiki'
    if site != "ar":
        if "Mr._Ibrahem" in editors:
            del editors["Mr._Ibrahem"]
        if "Mr. Ibrahem" in editors:
            del editors["Mr. Ibrahem"]
    # ---
    return editors


def work_in_one_site(site, links):
    # ---
    site = re.sub(r"wiki$", "", site)
    # ---
    printe.output(f"<<green>> site:{site} links: {len(links)}")
    # ---
    if len(links) < 100:
        printe.output("<<red>> less than 100 articles")
        # return
    # ---
    editors = get_editors(links, site)
    # ---
    editors = filter_editors(editors, site)
    # ---
    if not editors:
        printe.output("<<red>> no editors")
        return
    # ---
    if "dump" in sys.argv:
        print("json.dumps(editors, indent=2)")
        return
    # ---
    title = f"WikiProjectMed:WikiProject_Medicine/Stats/Top_medical_editors_{last_year}/{site}"
    # ---
    text = "{{:WPM:WikiProject Medicine/Total medical articles}}\n"
    text += f"{{{{Top medical editors by lang|{last_year}}}}}\n"
    # ---
    if site != "ar":
        text += f"Numbers of {last_year}. There are {len(links):,} articles in {site}\n"
    # ---
    text += """{| class="sortable wikitable"\n!#\n!User\n!Count\n|-"""
    # ---
    for i, (user, count) in enumerate(editors.items(), start=1):
        # ---
        user = user.replace("_", " ")
        # ---
        text += f"\n|-\n!{i}\n|[[:w:{site}:user:{user}|{user}]]\n|{count:,}"
        # ---
        if i == 100:
            break
        # ---
    # ---
    text += "\n|}"
    # ---
    page = md_MainPage(title, "www", family="mdwiki")
    p_text = page.get_text()
    # ---
    if p_text != text:
        page.save(newtext=text, summary="update", nocreate=0, minor="")
    else:
        printe.output("<<green>> no changes")
    # ---
    return editors


def start():
    # ---
    p_site = ""
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg == "site":
            p_site = value
    # ---
    # read json files in sites_dir
    files = os.listdir(sites_dir)
    # ---
    # sort files by biggest size
    files = sorted(files, key=lambda x: os.stat(sites_dir / x).st_size, reverse=True)
    # ---
    for numb, file in enumerate(files, start=1):
        # ---
        printe.output(f"<<green>> n: {numb} file: {file}:")
        # ---
        if not file.endswith("wiki.json"):
            continue
        # ---
        site = file[:-5]
        # ---
        if site in skip_sites:
            continue
        # ---
        if p_site and f"{p_site}wiki" != site:
            continue
        # ---
        with open(sites_dir / file, "r", encoding="utf-8") as f:
            links = json.load(f)
        # ---
        work_in_one_site(site, links)


if __name__ == "__main__":
    start()
