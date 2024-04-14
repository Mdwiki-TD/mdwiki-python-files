"""
from mass.radio.bots.add_cat import add_cat_to_images, add_cat_bot

"""
import sys
from multiprocessing import Pool
from newapi import printe
from newapi.ncc_page import CatDepth, NEW_API, MainPage as ncc_MainPage

api_new = NEW_API("www", family="nccommons")
api_new.Login_to_wiki()

study_done = []


def add(da=[], title="", cat=""):
    if da:
        title, cat = da[0], da[1]
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
    if text.find(cat) != -1:
        printe.output(f"cat {title} already has it.")
        return
    # ---
    newtext = text
    newtext += cat_line
    # ---
    page.save(newtext=newtext, summary=summary)


def mu(tab):
    pool = Pool(processes=3)
    pool.map(add, tab)
    pool.close()
    pool.terminate()


def add_cat_bot(pages, cat):
    if "multi" in sys.argv:
        tab = [[x, cat] for x in pages]
        mu(tab)
    else:
        for title in pages:
            add(title=title, cat=cat)


def add_cat_to_images(cat_list, cat_title):
    # ---
    done = CatDepth(cat_title, sitecode="www", family="nccommons", depth=0, ns="")
    # ---
    study_done.extend(done)
    # ---
    new_cat_list = [x for x in cat_list if x not in study_done and x not in done]
    # ---
    printe.output(f"{len(done)=}, {len(new_cat_list)=}")
    # ---
    add_cat_bot(new_cat_list, cat_title)