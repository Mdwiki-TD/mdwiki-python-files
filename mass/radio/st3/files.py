"""

python3 core8/pwb.py mass/radio/st3/files

tfj run files --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/files"

"""
import re
from newapi import printe
from newapi.ncc_page import CatDepth
from newapi.ncc_page import MainPage as ncc_MainPage
from mass.radio.lists.cases_to_cats import cases_cats# cases_cats()

def images_to_cats():
    members = CatDepth("Category:Radiopaedia_images_by_system", sitecode="www", family="nccommons", depth=1, ns="10")
    reg = r"^File:.*? \(Radiopaedia (\d+)\)\.\w+$"
    # ---
    tab = {}
    # ---
    for file in members:
        match = re.match(reg, file)
        if match:
            case_id = match.group(1)
            # ---
            tab[file] = case_id
    # ---
    print(f"images_to_cats, lenth of members: {len(members)} ")
    print(f"images_to_cats, lenth of tab: {len(tab)} ")

    return tab


def add(da=[], title="", cat=""):
    if da:
        title, cat = da[0], da[1]
    # ---
    page = ncc_MainPage(title, "www", family="nccommons")

    if not page.exists():
        return

    text = page.get_text()
    # ---
    if text.find(cat) != -1 or text.find("[[Category:Radiopaedia case") != -1:
        printe.output(f"cat {title} already has it.")
        return
    # ---
    newtext = text
    newtext += f"\n[[{cat}]]"
    # ---
    page.save(newtext=newtext, summary=f"Bot: added [[:{cat}]]")


def start():
    # ---
    cats = cases_cats()
    imgs = images_to_cats()
    # ---
    new = {x: cats[v] for x, v in imgs.items() if v in cats}
    # ---
    print(f"{len(new)=}")
    for numb, (file, cat) in enumerate(new.items(), start=1):
        # ---
        printe.output(f"{file=}: {cat=}")
        # ---
        add(title=file, cat=cat)


if __name__ == "__main__":
    start()
