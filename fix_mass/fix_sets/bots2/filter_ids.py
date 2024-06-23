"""

from fix_mass.fix_sets.bots2.filter_ids import filter_no_title

"""
import sys
from newapi import printe

from fix_mass.jsons.files import studies_titles, studies_titles2


def filter_no_title(ids):
    # ---
    ss_tt = studies_titles.copy()
    ss_tt.update(studies_titles2)
    # ---
    if not ids:
        printe.output("\t<<red>> filter_no_title, no ids. return {}")
        return {}
    # ---
    ids_titles = {study_id: ss_tt[study_id] for study_id in ids if study_id in ss_tt}
    # ---
    ids_no_title = [k for k in ids if k not in ids_titles]
    # ---
    if ids_no_title:
        printe.output(f" remove ids_no_title: {len(ids_no_title):,}")
        print("\t\t", ", ".join(ids_no_title))
    # ---
    printe.output(f"<<green>> len of ids: {len(ids):,}, after filter_no_title: {len(ids_titles):,}")
    # ---
    return ids_titles
