"""

from fix_mass.fix_sets.bots2.filter_ids import filter_no_title, filter_done

"""
import sys
from newapi import printe

from fix_mass.jsons.files import studies_titles
from fix_mass.fix_sets.bots2.done2 import find_done_study  # find_done_study(title)


def filter_no_title(ids):
    # ---
    ids_titles = {study_id: studies_titles[study_id] for study_id in ids if study_id in studies_titles}
    # ---
    ids_no_title = [k for k in ids if k not in ids_titles]
    # ---
    if ids_no_title:
        printe.output(f" remove ids_no_title: {len(ids_no_title):,}")
        print(", ".join(ids_no_title))
    # ---
    printe.output(f"<<green>> len of ids: {len(ids):,}, after filter_no_title: {len(ids_titles):,}")
    # ---
    return ids_titles


def filter_done(ids_titles):
    # ---
    if "nodone" in sys.argv:
        return ids_titles
    # ---
    already_done = [k for k, v in ids_titles.items() if find_done_study(v)]
    # ---
    printe.output(f"already_done: {len(already_done):,}")
    # ---
    ids_titles = {k: v for k, v in ids_titles.items() if k not in already_done}
    # ---
    printe.output(f"<<green>> ids_titles: {len(ids_titles):,}, after remove already_done..")
    # ---
    return ids_titles
