"""

tfj run stats --image python3.9 --command "$HOME/jobs/stats.sh"

python3 core8/pwb.py stats/all2 ask

"""
import json
import os
from pathlib import Path

from datetime import datetime

last_year = datetime.now().year - 1
# ---
from newapi import printe
from newapi.mdwiki_page import md_MainPage
from stats.editors import validate_ip

# ---
Dir = Path(__file__).parent
editors_dir = Dir / "editors"
# ---
skip_sites = ["enwiki", "wikidatawiki", "commonswiki", "specieswiki"]


def targets_text(targets):
    tt = '{| class="sortable wikitable floatright"\n|\n'
    tt += '<div style="max-height:250px; overflow: auto;vertical-align:top;font-size:90%;max-width:400px">\n'
    tt += "<pre>\n"
    # ---
    tt += targets
    # ---
    tt += "\n</pre>"
    tt += "\n</div>"
    tt += "\n|-\n|}"
    # ---
    return tt


def filter_editors(editors, site):
    # ---
    for x in editors.copy().keys():
        if validate_ip(x):
            del editors[x]
    # ---
    return editors


def work_all(editors):
    # ---
    editors = filter_editors(editors, "all")
    # ---
    if not editors:
        printe.output("<<red>> no editors")
        return
    # ---
    title = f"WikiProjectMed:WikiProject_Medicine/Stats/Top_medical_editors_{last_year}_(all)"
    # ---
    text = "{{:WPM:WikiProject Medicine/Total medical articles}}\n"
    text += f"{{{{Top medical editors by lang|{last_year}}}}}\n"
    # ---
    text += f"Numbers of {last_year}.\n"
    # ---
    txt_table = """{| class="sortable wikitable"\n!#\n!User\n!Count\n"""
    txt_table += """!Wiki\n"""
    # ---
    targets = ""
    # ---
    for i, (user, ta) in enumerate(editors.items(), start=1):
        # ---
        count = ta["count"]
        # ---
        wiki = ta["site"]
        # ---
        user = user.replace("_", " ")
        # ---
        # #{{#target:User:{User}|{wiki}.wikipedia.org}}
        targets += f"#{{{{#target:User:{user}|{wiki}.wikipedia.org}}}}\n"
        # ---
        txt_table += f"|-\n" f"!{i}\n" f"|[[:w:{wiki}:user:{user}|{user}]]\n" f"|{count:,}\n" f"|{wiki}\n"
        # ---
        # if i == 1000: break
        # ---
        if count < 10:
            break
        # ---
    # ---
    txt_table += "\n|}"
    # ---
    # add targets section
    text += targets_text(targets)
    # ---
    text += f"\n==users==\n{txt_table}"
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
    # read json files in editors_dir
    files = os.listdir(editors_dir)
    # ---
    all_editors = {}
    # ---
    for numb, file in enumerate(files, start=1):
        # ---
        printe.output(f"<<green>> n: {numb} file: {file}:")
        # ---
        if not file.endswith(".json"):
            continue
        # ---
        site = file[:-5]
        # ---
        print(f"{file=}, {site=}")
        # ---
        if f"{site}wiki" in skip_sites:
            continue
        # ---
        with open(editors_dir / f"{site}.json", "r", encoding="utf-8") as f:
            editors = json.load(f)
        # ---
        for user, count in editors.items():
            if user not in all_editors:
                all_editors[user] = {"count": count, "site": site}
            else:
                if all_editors[user]["count"] < count:
                    all_editors[user]["count"] = count
                    all_editors[user]["site"] = site
    # ---
    all_editors = dict(sorted(all_editors.items(), key=lambda x: x[1]["count"], reverse=True))
    # ---
    work_all(all_editors)


if __name__ == "__main__":
    start()
