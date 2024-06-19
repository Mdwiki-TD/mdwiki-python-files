"""
from mass.radio.bots.add_cat import add_cat_to_images, add_cat_bot

"""
import re
import sys
from multiprocessing import Pool
from newapi import printe
from newapi.ncc_page import CatDepth, NEW_API, MainPage as ncc_MainPage

api_new = NEW_API("www", family="nccommons")
api_new.Login_to_wiki()

study_done = []

skip_titles = [
    "File:Angiodysplasia - cecal active bleed (Radiopaedia 168775-136954 Coronal 91).jpeg",
]


def add(da=None, title="", cat="", cat2=""):
    if da:
        title, cat, cat2 = da[0], da[1], da[2]
    # ---
    if title.find("_") != -1:
        title = title.replace("_", " ")
    # ---
    if title in skip_titles:
        printe.output(f"Skipping {title}...")
        return
    # ---
    if not title or not cat:
        printe.output("no title or cat")
        return
    # ---
    cat_line = f"\n[[{cat}]]"
    summary = f"Bot: added [[:{cat}]]"
    # ---
    if "justadd" in sys.argv:
        added = api_new.Add_To_Bottom(cat_line, summary, title, poss="Bottom")
        printe.output(f"Added {title} to {cat}: result: {added}")
        return
    # ---
    page = ncc_MainPage(title, "www", family="nccommons")

    if not page.exists():
        return

    text = page.get_text()
    # ---
    newtext = text
    # ---
    if text.find(cat) != -1:
        printe.output(f"cat {title} already has it.")
        summary = f"Bot: remove [[:{cat2}]]"
        if "del2" not in sys.argv:
            return
    else:
        newtext += cat_line
    # ---
    if cat2 and "del2" in sys.argv:
        newtext = newtext.replace(f"[[{cat2}]]", "")
        # ---
        if newtext.find(f"[[{cat2}") != -1:
            for x in newtext.split("\n"):
                if x.startswith(f"[[{cat2}"):
                    newtext = newtext.replace(x, "")
                    break
    # ---
    page.save(newtext=newtext, summary=summary)


def mu(tab):
    pool = Pool(processes=3)
    pool.map(add, tab)
    pool.close()
    pool.terminate()


def add_cat_bot(pages, cattitle, cat2):
    if "multi" in sys.argv:
        tab = [[x, cattitle, cat2] for x in pages]
        mu(tab)
    else:
        for title in pages:
            add(title=title, cat=cattitle, cat2=cat2)


def add_cat_to_images(cat_list, cat_title, cat):
    # ---
    done = CatDepth(cat_title, sitecode="www", family="nccommons", depth=0, ns="")
    # ---
    study_done.extend(done)
    # ---
    new_cat_list = cat_list
    # ---
    if "del2" not in sys.argv:
        new_cat_list = [x for x in cat_list if x not in study_done and x not in done]
    # ---
    printe.output(f"{len(done)=}, {len(new_cat_list)=}")
    # ---
    add_cat_bot(new_cat_list, cat_title, cat)
